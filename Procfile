web: uvicorn app.main:app --host=0.0.0.0 --port=$PORT
worker: streamlit run app/frontend.py --server.port=$PORT --server.enableCORS=false 