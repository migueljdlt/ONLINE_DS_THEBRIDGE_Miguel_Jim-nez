import os
import sys
import time
import json
import argparse
import logging
from typing import Dict, Any, Optional, List

import requests
from requests.adapters import HTTPAdapter, Retry
from tqdm import tqdm


BASE_URL = "https://api.themoviedb.org/3"
DISCOVER_ENDPOINT = "/discover/movie"
MOVIE_ENDPOINT = "/movie/{movie_id}"
KEYWORDS_ENDPOINT = "/movie/{movie_id}/keywords"
CREDITS_ENDPOINT = "/movie/{movie_id}/credits"
RELEASE_DATES_ENDPOINT = "/movie/{movie_id}/release_dates"
VIDEOS_ENDPOINT = "/movie/{movie_id}/videos"
SIMILAR_ENDPOINT = "/movie/{movie_id}/similar"

REQUEST_PAUSE = 0.26


def make_session():
    session = requests.Session()
    retries = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504]
    )
    session.mount('https://', HTTPAdapter(max_retries=retries))
    return session


def robust_get(session, url, params, sleep_time=REQUEST_PAUSE):
    try:
        response = session.get(url, params=params, timeout=30)
        
        if response.status_code == 429:
            retry_after = response.headers.get('Retry-After', '5')
            wait_time = float(retry_after)
            logging.warning(f"Rate limit alcanzado. Esperando {wait_time}s...")
            time.sleep(wait_time)
            response = session.get(url, params=params, timeout=30)
        
        if response.status_code != 200:
            logging.warning(f"Request falló con status {response.status_code}")
            return None
        
        return response.json()
    
    except Exception as e:
        logging.error(f"Error en request: {e}")
        return None
    
    finally:
        time.sleep(sleep_time)


def discover_movies(api_key, session, discover_params, max_pages=None):
    movies = []
    page = 1
    
    while True:
        params = {'api_key': api_key, 'page': page}
        params.update(discover_params)
        
        url = BASE_URL + DISCOVER_ENDPOINT
        data = robust_get(session, url, params)
        
        if not data:
            logging.warning(f"No se obtuvieron datos en página {page}")
            break
        
        results = data.get('results', [])
        if not results:
            break
        
        movies.extend(results)
        total_pages = data.get('total_pages', 1)
        logging.info(f"Página {page}/{total_pages} procesada ({len(results)} películas)")
        
        page += 1
        if max_pages and page > max_pages:
            break
        if page > total_pages:
            break
    
    return movies


def fetch_movie_details(api_key, session, movie_id, language='en-US'):
    url = BASE_URL + MOVIE_ENDPOINT.format(movie_id=movie_id)
    params = {'api_key': api_key, 'language': language}
    return robust_get(session, url, params)


def fetch_movie_keywords(api_key, session, movie_id):
    url = BASE_URL + KEYWORDS_ENDPOINT.format(movie_id=movie_id)
    params = {'api_key': api_key}
    return robust_get(session, url, params)


def fetch_movie_credits(api_key, session, movie_id):
    url = BASE_URL + CREDITS_ENDPOINT.format(movie_id=movie_id)
    params = {'api_key': api_key}
    return robust_get(session, url, params)


def fetch_movie_release_dates(api_key, session, movie_id):
    url = BASE_URL + RELEASE_DATES_ENDPOINT.format(movie_id=movie_id)
    params = {'api_key': api_key}
    return robust_get(session, url, params)


def fetch_movie_videos(api_key, session, movie_id):
    url = BASE_URL + VIDEOS_ENDPOINT.format(movie_id=movie_id)
    params = {'api_key': api_key}
    return robust_get(session, url, params)


def fetch_similar_movies(api_key, session, movie_id, language='en-US'):
    url = BASE_URL + SIMILAR_ENDPOINT.format(movie_id=movie_id)
    params = {'api_key': api_key, 'language': language, 'page': 1}
    return robust_get(session, url, params)


def write_ndjson_line(path, obj):
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    with open(path, 'a', encoding='utf-8') as f:
        f.write(json.dumps(obj, ensure_ascii=False) + '\n')


def read_checkpoint(path):
    if not os.path.exists(path):
        return set()
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return set(json.load(f))
    except Exception:
        return set()


def save_checkpoint(path, processed_ids):
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(list(processed_ids), f)


def parse_discover_params(raw):
    params = {}
    if not raw:
        return params
    
    for part in raw.split('&'):
        if '=' in part:
            key, value = part.split('=', 1)
            params[key] = value
    
    return params


def main():
    parser = argparse.ArgumentParser(description='Extrae datos de películas desde TMDB API')
    
    parser.add_argument('--api-key', '-k', type=str, default=os.environ.get('TMDB_API_KEY'))
    parser.add_argument('--out', '-o', type=str, default='data/movies.ndjson')
    parser.add_argument('--checkpoint', type=str, default='data/checkpoint.json')
    parser.add_argument('--keywords', action='store_true')
    parser.add_argument('--credits', action='store_true')
    parser.add_argument('--release-dates', action='store_true')
    parser.add_argument('--videos', action='store_true')
    parser.add_argument('--similar', action='store_true')
    parser.add_argument('--all-extras', action='store_true')
    parser.add_argument('--max-pages', type=int, default=150)
    parser.add_argument('--discover-params', type=str, default='primary_release_date.gte=2010-01-01&primary_release_date.lte=2025-11-16&vote_count.gte=50')
    parser.add_argument('--limit-movies', type=int, default=None)
    parser.add_argument('--language', type=str, default='en-US')
    parser.add_argument('--pause', type=float, default=REQUEST_PAUSE)
    
    args = parser.parse_args()
    
    if not args.api_key:
        logging.error('API key no proporcionada')
        sys.exit(1)
    
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    if args.all_extras:
        args.keywords = True
        args.credits = True
        args.release_dates = True
        args.videos = True
        args.similar = True
    
    discover_params = parse_discover_params(args.discover_params)
    session = make_session()
    
    logging.info('Iniciando fase de discover...')
    discovered_movies = discover_movies(args.api_key, session, discover_params, max_pages=args.max_pages)
    logging.info(f'Total de películas descubiertas: {len(discovered_movies)}')
    
    if args.limit_movies:
        discovered_movies = discovered_movies[:args.limit_movies]
    
    processed_ids = read_checkpoint(args.checkpoint)
    movies_to_process = [m for m in discovered_movies if str(m.get('id')) not in processed_ids]
    
    logging.info(f'Películas pendientes de procesar: {len(movies_to_process)}')
    
    active_endpoints = ['details']
    if args.keywords:
        active_endpoints.append('keywords')
    if args.credits:
        active_endpoints.append('credits')
    if args.release_dates:
        active_endpoints.append('release_dates')
    if args.videos:
        active_endpoints.append('videos')
    if args.similar:
        active_endpoints.append('similar')
    
    logging.info(f'Endpoints activos: {", ".join(active_endpoints)}')
    
    progress_bar = tqdm(total=len(movies_to_process), desc='Procesando películas')
    
    for movie in movies_to_process:
        movie_id = movie.get('id')
        
        if not movie_id:
            progress_bar.update(1)
            continue
        
        details = fetch_movie_details(args.api_key, session, movie_id, args.language)
        
        if not details:
            logging.warning(f'No se obtuvieron detalles para película {movie_id}')
            processed_ids.add(str(movie_id))
            save_checkpoint(args.checkpoint, processed_ids)
            progress_bar.update(1)
            continue
        
        record = {
            'id': details.get('id'),
            'title': details.get('title'),
            'original_title': details.get('original_title'),
            'original_language': details.get('original_language'),
            'release_date': details.get('release_date'),
            'budget': details.get('budget'),
            'revenue': details.get('revenue'),
            'runtime': details.get('runtime'),
            'genres': details.get('genres'),
            'production_companies': details.get('production_companies'),
            'production_countries': details.get('production_countries'),
            'spoken_languages': details.get('spoken_languages'),
            'popularity': details.get('popularity'),
            'vote_average': details.get('vote_average'),
            'vote_count': details.get('vote_count'),
            'status': details.get('status'),
            'homepage': details.get('homepage'),
            'imdb_id': details.get('imdb_id'),
            'tagline': details.get('tagline'),
            'overview': details.get('overview'),
            'poster_path': details.get('poster_path'),
            'backdrop_path': details.get('backdrop_path'),
            'belongs_to_collection': details.get('belongs_to_collection'),
        }
        
        if args.keywords:
            keywords_data = fetch_movie_keywords(args.api_key, session, movie_id)
            record['keywords'] = keywords_data.get('keywords') if keywords_data else None
        
        if args.credits:
            credits_data = fetch_movie_credits(args.api_key, session, movie_id)
            if credits_data:
                record['cast'] = credits_data.get('cast', [])
                record['crew'] = credits_data.get('crew', [])
            else:
                record['cast'] = None
                record['crew'] = None
        
        if args.release_dates:
            release_data = fetch_movie_release_dates(args.api_key, session, movie_id)
            record['release_dates'] = release_data.get('results') if release_data else None
        
        if args.videos:
            videos_data = fetch_movie_videos(args.api_key, session, movie_id)
            record['videos'] = videos_data.get('results') if videos_data else None
        
        if args.similar:
            similar_data = fetch_similar_movies(args.api_key, session, movie_id, args.language)
            record['similar_movies'] = similar_data.get('results') if similar_data else None
        
        record['_discover_data'] = movie
        
        write_ndjson_line(args.out, record)
        
        processed_ids.add(str(movie_id))
        if len(processed_ids) % 50 == 0:
            save_checkpoint(args.checkpoint, processed_ids)
        
        progress_bar.update(1)
    
    progress_bar.close()
    save_checkpoint(args.checkpoint, processed_ids)
    
    logging.info(f'Extracción completada. Datos guardados en: {args.out}')
    logging.info(f'Total de películas procesadas: {len(processed_ids)}')


if __name__ == '__main__':
    main()
