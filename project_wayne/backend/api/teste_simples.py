print("=== TESTE DO AMBIENTE ===")

try:
    import flask
    print("✅ Flask OK")
except ImportError as e:
    print(f"❌ Flask erro: {e}")

try:
    import jwt
    print("✅ JWT OK") 
except ImportError as e:
    print(f"❌ JWT erro: {e}")

try:
    from flask_jwt_extended import JWTManager
    print("✅ Flask-JWT-Extended OK")
except ImportError as e:
    print(f"❌ Flask-JWT-Extended erro: {e}")

print("🎯 Teste concluído!")
