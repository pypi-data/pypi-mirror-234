from flask import request, Flask, redirect, session, render_template
from functools import wraps
from cardboard import Cardboard, CardboardAsync
import aiohttp, asyncio, time, warnings
import concurrent.futures

class FlaskIntegration:
    """
    A flask integration for Cardboard.

    Args:
        - app: Your Flask app.
        - cardboard: Your Cardboard app. Can be either the normal version or async version; it doesn't matter.
        - session_prefix: The session name where you store the cardboard authentication data. Defaults to "cardboard_"
            - token (eg. "cardboard_token")
            - refresh (eg. "cardboard_prefix")
            - expiry (eg. "cardboard_expiry")
            - rd (eg. "cardboard_rd")
            - cache (eg. "cardboard_cache")
        - login_url: A custom login URL instead of your Cardboard app's default URL.
        - redirect_template: A custom redirect template usable for metadata. A Flask variable {{ redirect }} will be passed for the redirect url!
    """
    def __init__(self, app:Flask, cardboard:Cardboard|CardboardAsync, session_prefix:str="cardboard_", login_url:str=None, redirect_template:str=None):
        self.app:Flask = app
        self.cb:Cardboard|CardboardAsync = cardboard
        self.secret = self.cb.secret
        self.client_id = self.cb.client_id
        self.cb = CardboardAsync(client_id=self.client_id, secret=self.secret)
        self.cbsync = concurrent.futures.ThreadPoolExecutor().submit(lambda: Cardboard(client_id=self.client_id, secret=self.secret)).result()
        self.session_token = f"{session_prefix}token"
        self.session_refresh = f"{session_prefix}refresh"
        self.session_expiry = f"{session_prefix}expiry"
        self.session_rd = f"{session_prefix}rd"
        self.session_cache = f"{session_prefix}cache"
        self.redirect_template = redirect_template

        self.app_login_redirect = self.cb.app_url if not login_url else login_url

        if not app.secret_key:
            raise ValueError("Flask app secret key is not set or is empty.")
    
    def _constructAuthToken(self, token, expiry, refresh):
        """
        Constructs an AuthToken class.
        """
        data = {"access_token": token, "refresh_token": refresh, "expires_in": expiry-round(time.time()), "token_type": "Bearer"}
        return self.cb.AuthToken(data=data)

    def getloop(self):
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        return loop

    async def asyncpost(self, url, data=None, headers=None) -> dict|int:
        """
        Makes a post request. Returns json or int.
        """
        async with aiohttp.ClientSession() as cs:
            async with cs.post(url, data=data, headers=headers) as response:
                return await response.json() if response.status == 200 else response.status
    
    def autologin(self, route_function):
        """
        Automatically logs you in with a token, or else redirects you to the app login page. This is async.

        Returns an AuthToken class. You can get the token with token.token

        Will automatically redirect after all processing in the login function is complete if the user came from a route with the loggedin decorator.
        
        Usage:

            ```@app.route('/login')
            @fi.autologin
            def login(token:AuthToken):
                # run code, with token always valid.
            ```
        """
        @wraps(route_function)
        def decorator(*args, **kwargs):
            cache = session.get(self.session_cache)
            if type(cache) == dict and round(time.time()) < cache.get("time")+60:
                result = route_function(self._constructAuthToken(cache.get("token"), session.get(self.session_expiry), session.get(self.session_refresh)), *args, **kwargs)
                if session.get(self.session_rd):
                    a = session.pop(self.session_rd)
                    if self.redirect_template:
                        return render_template(self.redirect_template, redirect=a)
                    return redirect(a)
                return result
            else:
                session[self.session_cache] = None
            code = request.args.get('code')
            thetoken = session.get(self.session_token)
            if thetoken and concurrent.futures.ThreadPoolExecutor().submit(lambda: self.cbsync.check_token(thetoken)).result():
                token = thetoken
                if session.get(self.session_expiry) and session.get(self.session_refresh):
                    token = self._constructAuthToken(token, session.get(self.session_expiry), session.get(self.session_refresh))
                elif session.get(self.session_refresh):
                    loop = self.getloop()
                    try:
                        token = loop.run_until_complete(self.cb.refresh_token(session.get(self.session_refresh)))
                    except:
                        if self.redirect_template:
                            return render_template(self.redirect_template, redirect=self.app_login_redirect)
                        return redirect(self.app_login_redirect)
                result = route_function(token, *args, **kwargs)
                session[self.session_cache] = {"time": round(time.time()), "token": token.token}
                if session.get(self.session_rd):
                    a = session.pop(self.session_rd)
                    if self.redirect_template:
                        return render_template(self.redirect_template, redirect=a)
                    return redirect(a)
                return result
            if code:
                grant_type = "authorization_code"
                data = {
                    "code": code,
                    "client_id": self.client_id,
                    "client_secret": self.secret,
                    "grant_type": grant_type,
                }
                loop = self.getloop()
                response = loop.run_until_complete(self.asyncpost(f"{self.cb._baseurl}/token", data=data, headers={"Content-Type": "application/x-www-form-urlencoded"}))
                if type(response) == int:
                    if self.redirect_template:
                        return render_template(self.redirect_template, redirect=self.app_login_redirect)
                    return redirect(self.app_login_redirect)
                token = self.cb.AuthToken(response)
            else:
                if self.redirect_template:
                    return render_template(self.redirect_template, redirect=self.app_login_redirect)
                return redirect(self.app_login_redirect)
            session[self.session_token] = token.token
            session[self.session_expiry] = round(time.time())+token.expires_in
            session[self.session_refresh] = token.refresh_token
            session[self.session_cache] = {"time": round(time.time()), "token": token.token}
            result = route_function(token, *args, **kwargs)
            if session.get(self.session_rd):
                a = session.pop(self.session_rd)
                if self.redirect_template:
                    return render_template(self.redirect_template, redirect=a)
                return redirect(a)
            return result
        return decorator

    def login_code(self, route_function):
        """
        Automatically passes the "code" variable instead of using request.args.get('code').

        Returns None if logged in.

        Does not validate your code; a fake code may be passed.

        ```diff
        - WARNING - Deprecated decorator!
        ```

        Usage:

            ```@app.route('/login')
            @fi.login_code
            def login(code:str|None, *args, **kwargs):
                # your login function.
            ```
        """
        warnings.warn("Deprecated decorator. Please use the autologin decorator instead.", DeprecationWarning)
        @wraps(route_function)
        def decorator(*args, **kwargs):
            thetoken = session.get(self.session_token)
            if thetoken and concurrent.futures.ThreadPoolExecutor().submit(lambda: self.cbsync.check_token(thetoken)).result():
                return route_function(None, *args, **kwargs)
            code = request.args.get('code')
            if not code:
                return redirect(self.app_login_redirect)
            return route_function(code, *args, **kwargs)
        return decorator
    
    def login_autoexchange(self, route_function):
        """
        Automatically exchanges the initial code. This is async.

        Returns None if invalid initial code.

        ```diff
        - WARNING - Deprecated decorator!
        ```

        Usage:

            ```@app.route('/login')
            @fi.login_autoexchange
            def login(token:AuthToken|None, *args, **kwargs):
                # your login function.
            ```
        """
        warnings.warn("Deprecated decorator. Please use the autologin decorator instead.", DeprecationWarning)
        @wraps(route_function)
        def decorator(*args, **kwargs):
            code = request.args.get('code')
            thetoken = session.get(self.session_token)
            if thetoken and concurrent.futures.ThreadPoolExecutor().submit(lambda: self.cbsync.check_token(thetoken)).result():
                token = thetoken
                return route_function(token, *args, **kwargs)
            if code:
                grant_type = "authorization_code"
                data = {
                    "code": code,
                    "client_id": self.client_id,
                    "client_secret": self.secret,
                    "grant_type": grant_type,
                }
                loop = self.getloop()
                response = loop.run_until_complete(self.asyncpost(f"{self.cb._baseurl}/token", data=data, headers={"Content-Type": "application/x-www-form-urlencoded"}))
                if type(response) == int:
                    token = None
                else:
                    token = self.cb.AuthToken(response)
            else:
                token = None
            return route_function(token, *args, **kwargs)
        return decorator

    def optional_logged_in(self, route_function):
        """
        Checks if the user is logged in with a valid auth token. Returns None if not valid.
        
        Checking is done in a seperate thread.

        Usage:

            ```@app.route('/home')
            @fi.optional_ogged_in
            def home(token:AuthToken|None, *args, **kwargs):
                # your function
            ```
        """
        @wraps(route_function)
        def decorator(*args, **kwargs):
            thetoken = session.get(self.session_token)
            cache = session.get(self.session_cache)
            if type(cache) == dict and round(time.time()) < cache.get("time")+60:
                return route_function(self._constructAuthToken(cache.get("token"), session.get(self.session_expiry), session.get(self.session_refresh)), *args, **kwargs)
            else:
                session[self.session_cache] = None
            if thetoken and concurrent.futures.ThreadPoolExecutor().submit(lambda: self.cbsync.check_token(thetoken)).result():
                token = session.get(self.session_token)
                if session.get(self.session_expiry) and session.get(self.session_refresh):
                    token = self._constructAuthToken(token, session.get(self.session_expiry), session.get(self.session_refresh))
                elif session.get(self.session_refresh):
                    loop = self.getloop()
                    try:
                        token = loop.run_until_complete(self.cb.refresh_token(session.get(self.session_refresh)))
                        session[self.session_cache] = {"time": round(time.time()), "token": token.token}
                    except:
                        return route_function(None, *args, **kwargs)
                return route_function(token, *args, **kwargs)
            else:
                return route_function(None, *args, **kwargs)
        return decorator

    def logged_in(self, route_function):
        """
        Checks if the user is logged in with a valid auth token. Redirects to the app login if not valid.

        After logging in, the user is redirected back to the original URL if the @autologin route is used.
        
        Checking is done in a seperate thread.

        Usage:

            ```@app.route('/dashboard')
            @fi.logged_in
            def dashboard(token:AuthToken, *args, **kwargs):
                # your function
            ```
        """
        @wraps(route_function)
        def decorator(*args, **kwargs):
            thetoken = session.get(self.session_token)
            cache = session.get(self.session_cache)
            if type(cache) == dict and round(time.time()) < cache.get("time")+60:
                return route_function(self._constructAuthToken(cache.get("token"), session.get(self.session_expiry), session.get(self.session_refresh)), *args, **kwargs)
            else:
                session[self.session_cache] = None
            if thetoken and concurrent.futures.ThreadPoolExecutor().submit(lambda: self.cbsync.check_token(thetoken)).result():
                token = session.get(self.session_token)
                if session.get(self.session_expiry) and session.get(self.session_refresh):
                    token = self._constructAuthToken(token, session.get(self.session_expiry), session.get(self.session_refresh))
                    session[self.session_cache] = {"time": round(time.time()), "token": token.token}
                elif session.get(self.session_refresh):
                    loop = self.getloop()
                    try:
                        token = loop.run_until_complete(self.cb.refresh_token(session.get(self.session_refresh)))
                        session[self.session_cache] = {"time": round(time.time()), "token": token.token}
                    except:
                        session[self.session_rd] = request.url
                        if self.redirect_template:
                            return render_template(self.redirect_template, redirect=self.app_login_redirect)
                        return redirect(self.app_login_redirect)
                return route_function(token, *args, **kwargs)
            else:
                session[self.session_rd] = request.url
                if self.redirect_template:
                    return render_template(self.redirect_template, redirect=self.app_login_redirect)
                return redirect(self.app_login_redirect)
        return decorator
    
    def autologout(self, route_function):
        """
        Automatically logs the user out, removing all necessary session data.

        Usage:

            ```@app.route('/logout')
            @fi.autologout
            def logout(*args, **kwargs):
                return redirect(url_for('home'))
            ```
        """
        @wraps(route_function)
        def decorator(*args, **kwargs):
            ot = session.pop(self.session_token, None)
            session.pop(self.session_expiry, None)
            session.pop(self.session_refresh, None)
            session.pop(self.session_rd, None)
            session.pop(self.session_cache, None)
            if ot:
                try:
                    concurrent.futures.ThreadPoolExecutor().submit(lambda: self.cbsync.revoke_token(ot)).result()
                except:
                    pass
            return route_function(*args, **kwargs)
        return decorator