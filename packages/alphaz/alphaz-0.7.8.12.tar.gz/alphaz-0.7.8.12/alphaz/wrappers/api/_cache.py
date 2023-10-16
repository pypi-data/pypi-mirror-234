import datetime, functools

# FLASK
from flask import request

"""Exemple:

@api.route("/pages", methods=["GET"])
@with_cache(timeout=10)  # Exemple avec un timeout de 10 minutes
def get_all_yamls():
    # Remplacez ceci par votre logique pour obtenir les données
    return jsonify(get_topics())
"""

cache = {}


def with_cache(func=None, *, timeout=None):
    if func is None:
        return lambda func: with_cache(func, timeout=timeout)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Vérifiez si reset_cache est True
        reset_cache = request.args.get("reset_cache", "false").lower() == "true"

        # Si reset_cache est True, ignorez le cache
        if reset_cache:
            return func(*args, **kwargs)
        print("   > Load cache", func, args, kwargs)

        # Sinon, vérifiez si les données sont dans le cache
        cache_key = func.__name__
        if cache_key in cache:
            data, timestamp = cache[cache_key]
            # Vérifiez si les données ont expiré
            if (
                timeout
                and (datetime.datetime.now() - timestamp).total_seconds() > timeout * 60
            ):
                # Les données ont expiré, rechargez-les
                result = func(*args, **kwargs)
                cache[cache_key] = (result, datetime.datetime.now())
                return result
            return data

        # Si les données ne sont pas dans le cache, chargez-les et stockez-les dans le cache
        result = func(*args, **kwargs)
        cache[cache_key] = (result, datetime.datetime.now())
        return result

    return wrapper
