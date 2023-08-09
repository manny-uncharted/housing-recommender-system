mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"yvannbarbotts@gmail.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
\n\
[theme]\n\
base = \"light\"\n\
primaryColor = \"#89CFA6\"\n\
backgroundColor = \"#E0F8CE\"\n\
secondaryBackgroundColor = \"#FFACE4\"\n\
textColor = \"#000900\"\n\
font = \"sans serif\"\n\
" > ~/.streamlit/config.toml
