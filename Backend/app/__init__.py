"""
AeroGuard Flask Application Factory

This module initializes the Flask application with all necessary
configurations, blueprints, error handlers, and middleware.

Architecture:
    - Application Factory Pattern: Enables multiple app instances with different configs
    - Blueprint Pattern: Modular route organization (health, forecast, model, comparison)
    - Middleware Pattern: Request logging, CORS, error handling
    - Service Layer: Decoupled business logic from routes

Usage:
    >>> from app import create_app
    >>> app = create_app()
    >>> app.run()

Example with custom config:
    >>> from app.config import DevelopmentConfig
    >>> app = create_app(DevelopmentConfig)
"""

import logging
from flask import Flask, app
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from app.config import Config
from app.database import init_db
from app.utils.error_handlers import register_error_handlers
from app.routes import health, forecast, model
from app.routes.model_comparison import model_comparison_bp
from flask_jwt_extended import JWTManager

logger = logging.getLogger(__name__)

# Initialize rate limiter (will be configured in create_app)
limiter = Limiter(
    key_func=get_remote_address,  # Rate limit by IP address
    default_limits=["200 per day", "50 per hour"],  # Global default limits
    storage_uri="memory://",  # Use in-memory storage (Redis for production scale)
)


def create_app(config_class=None):
    """
    Application factory function.

    Creates and configures the Flask application with all necessary:
    - Configuration settings
    - CORS middleware
    - Blueprint routes
    - Error handlers
    - Request/response middleware

    Args:
        config_class (class, optional): Configuration class to use.
            Defaults to Config. Common options:
            - Config: Base configuration
            - DevelopmentConfig: Development with debug enabled
            - ProductionConfig: Production with security hardening
            - TestingConfig: Testing with in-memory database

    Returns:
        Flask: Configured Flask application instance ready to serve requests

    Raises:
        ImportError: If configuration class cannot be imported
        ValueError: If required settings are missing in production

    Example:
        >>> from app import create_app
        >>> from app.config import DevelopmentConfig
        >>> app = create_app(DevelopmentConfig)
        >>> app.run(debug=True)
    """
    if config_class is None:
        config_class = Config

    # Create Flask app instance
    app = Flask(__name__)
    logger.debug(f"Creating Flask app with config: {config_class.__name__}")

    try:
        # Load configuration
        app.config.from_object(config_class)
        logger.info(f"✓ Configuration loaded: {config_class.__name__}")

        # Initialize JWT
        jwt = JWTManager()
        jwt.init_app(app)

        # Initialize rate limiter
        limiter.init_app(app)
        logger.info("✓ Rate limiter initialized (200/day, 50/hour global)")

        # Initialize database
        init_db(app)

        # Initialize CORS (Cross-Origin Resource Sharing)
        _setup_cors(app)

        # Register error handlers (400, 401, 403, 404, 405, 500, 503, etc.)
        _register_error_handlers(app)

        # Register route blueprints
        _register_blueprints(app)

        # Register request/response hooks
        _register_hooks(app)

        logger.info("✓ Application factory complete - all components initialized")

    except Exception as e:
        logger.error(f"✗ Failed to create application: {e}", exc_info=True)
        raise

    return app


def _setup_cors(app):
    """
    Configure CORS (Cross-Origin Resource Sharing).

    Allows:
    - Specified origins only (from CORS_ORIGINS config)
    - Common methods (GET, POST, PUT, DELETE, OPTIONS)
    - Common headers (Content-Type, Authorization)
    - Credentials (cookies, authorization headers)

    Args:
        app (Flask): Flask application instance
    """
    try:
        cors_config = {
            "origins": app.config.get("CORS_ORIGINS", "*"),
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "expose_headers": ["X-Request-ID", "X-Response-Time"],
            "supports_credentials": True,
            "max_age": 3600
        }
        
        CORS(app, resources={r"/*": cors_config})
        logger.info(f"✓ CORS initialized with origins: {cors_config['origins']}")
    except Exception as e:
        logger.error(f"✗ CORS initialization failed: {e}")
        raise


def _register_error_handlers(app):
    """
    Register global error handlers.

    Handles:
    - 400: Bad Request (validation errors)
    - 401: Unauthorized (authentication errors)
    - 403: Forbidden (authorization errors)
    - 404: Not Found (missing endpoints)
    - 405: Method Not Allowed
    - 500: Internal Server Error
    - 503: Service Unavailable

    Args:
        app (Flask): Flask application instance
    """
    try:
        register_error_handlers(app)
        logger.info("✓ Error handlers registered")
    except Exception as e:
        logger.error(f"✗ Error handler registration failed: {e}")
        raise


def _register_blueprints(app):
    """
    Register all route blueprints with specific rate limits.

    Blueprints:
    - health.bp: Health check and status endpoints (/) - NO RATE LIMIT
    - forecast.bp: Air quality forecasting (/api/v1/forecast) - 10/min (expensive ML)
    - model.bp: Model management (/api/v1/model) - 20/min
    - model_comparison_bp: Model comparison (/api/v1/model/compare) - 5/min (very expensive)
    - realtime_aqi.bp: Real-time AQI data (/api/v1/realtime-aqi) - 30/min
    - user_routes.bp: User management - 5/min for register/login
    - generative_ai.bp: AI explanations - 10/min (API calls)
    - analytics_bp.bp: Analytics - 30/min
    - historical_analysis.bp: Historical data - 20/min
    - health_risk.bp: Health risk assessment - 20/min

    Args:
        app (Flask): Flask application instance
    """
    from app.routes import user as user_routes
    from app.routes import realtime_aqi as realtime_aqi_routes
    from app.routes import generative_ai as generative_ai_routes
    from app.routes import analytics_route as analytics_bp
    from app.routes import historical_analysis as historical_analysis_routes
    from app.routes import health_risk as health_risk_routes

    # Exempt health endpoints from rate limiting
    limiter.exempt(health.bp)

    blueprints = [
        (health.bp, "Health Check", None),  # No limit
        (forecast.bp, "Forecast", "10 per minute"),
        (model.bp, "Model Management", "20 per minute"),
        (model_comparison_bp, "Model Comparison", "5 per minute"),
        (user_routes.bp, "User API", "20 per minute"),
        (realtime_aqi_routes.bp, "Real-time AQI", "30 per minute"),
        (generative_ai_routes.bp, "Generative AI", "10 per minute"),
        (analytics_bp.bp, "Analytics", "30 per minute"),
        (historical_analysis_routes.bp, "Historical Analysis", "20 per minute"),
        (health_risk_routes.bp, "Health Risk Assessment", "20 per minute")
    ]

    try:
        for blueprint, name, rate_limit in blueprints:
            app.register_blueprint(blueprint)
            prefix = getattr(blueprint, "url_prefix", None) or "/"
            
            # Apply rate limit to blueprint if specified
            if rate_limit:
                limiter.limit(rate_limit)(blueprint)
                logger.info(f"  ✓ {name:25} -> {prefix:30} (limit: {rate_limit})")
            else:
                logger.info(f"  ✓ {name:25} -> {prefix:30} (no limit)")
        
        logger.info("✓ All blueprints registered with rate limits")
    except Exception as e:
        logger.error(f"✗ Blueprint registration failed: {e}")
        raise


def _register_hooks(app):
    """
    Register request/response middleware hooks.

    Hooks:
    - before_request: Log incoming requests and generate request ID
    - after_request: Add response headers, log response times

    Args:
        app (Flask): Flask application instance
    """
    import time
    import uuid
    from flask import request, g

    @app.before_request
    def before_request():
        """Log incoming request details and generate request ID."""
        g.start_time = time.time()
        g.request_id = str(uuid.uuid4())
        
        # Sanitize query params for logging (remove sensitive data)
        safe_args = {k: v for k, v in request.args.items() 
                     if k.lower() not in ['password', 'token', 'api_key', 'secret', 'key']}
        
        logger.debug(f"→ {request.method:6} {request.path} [ID: {g.request_id}] params={safe_args}")

    @app.after_request
    def after_request(response):
        """Log response details and add security headers."""
        # Calculate response time
        duration = time.time() - getattr(g, "start_time", 0)

        # Add response headers
        response.headers["X-Request-ID"] = getattr(g, "request_id", str(uuid.uuid4()))
        response.headers["X-Response-Time"] = f"{duration:.6f}"
        
        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        # HSTS in production
        if app.config.get("ENV") == "production":
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        # Remove server identification
        response.headers.pop("Server", None)

        logger.debug(f"← {response.status_code:3} {request.path} ({duration:.3f}s)")
        return response

    logger.info("✓ Request/response hooks registered")
