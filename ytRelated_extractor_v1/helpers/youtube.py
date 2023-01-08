from dotenv import load_dotenv # biblioteca para ler arquivo .env no diretório do projeto e acessar chave de API
import os # biblioteca utilizada para resgatar chave de API salva como variável de ambiente
from googleapiclient.discovery import build # cliente python para consumo da youtube Data API v3

# Resgatando chave de API de inicializando cliente
load_dotenv('/content/drive/MyDrive/Colab Notebooks/youTube/.env')
API_KEY = os.environ['API_KEY']
youtube = build('youtube','v3', developerKey=API_KEY)

##### DEFINIÇÃO DAS FUNÇÕES #####

# 1. Função para extrair a id de um vídeo a partir da sua url:
def get_video_id(video_link):
    sliced_link = video_link[:-12:-1]

    return sliced_link[::-1]
    # Obs. No futuro, pretendo implementar essa função utilizando Regex.
    # Nem sempre os últimos 11 caracteres da URL correspondem ao id do
    # vídeo.

# 2. Funções para requisitar dados da api:
## 2.1. Pesquisa os vídeos relacionados em relação a um vídeo arbitrário definido pelo usuário
def basic_search(seed):
    try:
        print(f'extracting coords for video {seed}...')
        request = youtube.search().list(
            part="snippet",
            maxResults=10,
            relatedToVideoId=seed,
            type="video"
        ).execute()
        print('ok!')

        data = request.get('items')

        related_ids = list(map(lambda x: x['id']['videoId'], data))
        source = [seed] * len(related_ids)
        target = related_ids.copy()

        return {'source': source, 'target': target}, related_ids

    except Exception as e:
        print(e)

## 2.2. Pesquisa os vídeos relacionados em relação a um conjunto de vídeos. Função utilizada
##      durante as iterações.
def deep_search(seeds):
    for seed in seeds:
        yield basic_search(seed)

## 2.3. Pesquisa os detalhes de um vídeo (visualizações, likes, comentários) a partir da sua
##      id. 
def get_video_details(seed):
  try:
    res = youtube.videos().list(part='statistics,snippet', id=seed).execute()
    data = res.get('items')[0]

    statistics = data['statistics']
    
    # Alguns vídeos por configuração de privacidade, não retornam dados como quantidade
    # de views, likes ou comentários. Por isso é preciso fazer essas verificações para
    # não quebrar o código no meio da execução
    if 'viewCount' in statistics:
      views = int(statistics['viewCount'])
    else:
      views = 0 # caso essas estatísticas não estejam disponíveis, vamos completar automaticamente com 0.

    if 'likeCount' in statistics:
      likes = int(statistics['likeCount'])
    else:
      likes = 0

    if 'commentCount' in statistics:
      comments = int(statistics['commentCount'])
    else:
      comments = 0
    
    # Vamos retornar um dicionário com as informações coletadas
    return {
        'videoId' : data['id'],
        'title' : data['snippet']['title'],
        'description' : data['snippet']['description'],
        'publishedAt' : data['snippet']['publishedAt'],
        'channelId' : data['snippet']['channelId'],
        'channelTitle' : data['snippet']['channelTitle'],
        'views' : views,
        'likes' : likes,
        'comments' : comments
    }
  # Se não for possível obter nenhuma informação do vídeo, vamos retornar o mesmo dicionário, mas
  # com valores 'null' para as variáveis não obtidas.  
  except:
      return {
        'videoId' : seed,
        'title' : 'null',
        'description' : 'null',
        'publishedAt' : 'null',
        'channelId' : 'null',
        'channelTitle' : 'null',
        'views' : 'null',
        'likes' : 'null',
        'comments' : 'null'
      }
