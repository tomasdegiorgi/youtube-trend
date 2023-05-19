
from googleapiclient.discovery import build
from datetime import datetime, timedelta

api_key = 'api_key'

youtube = build('youtube', 'v3', developerKey=api_key)

now = datetime.now()
one_week_ago = (now - timedelta(days=30)).isoformat("T") + "Z"

search_response_canales = youtube.search().list(part='snippet', maxResults='50', q='minecraft', type='video').execute()

canales = []

#ELEGIR CANALES

for search_result_canales in search_response_canales.get("items",[]):
    if search_result_canales['id']['kind'] == 'youtube#video':
        #CARGA DE CANALES
        canales.append(search_result_canales['snippet']['channelId'])
#ELIMINACION DE REPETIDOS
canales = list(dict.fromkeys(canales))

canal_porcentajes = []
visitas_video_max = 0

#FILTRAR VIDEOS DE LOS CANALES
#VA CANAL POR CANAL
for canal in canales:
    #FILTRA ULTIMOS VIDEOS DE LA ULTIMA SEMANA
    search_response_videos = youtube.search().list(part='snippet', channelId=canal, order='date', publishedAfter=one_week_ago,type='video').execute()
    #RECORRE VIDEO POR VIDEO 
    cantidad_videos = 0
    total_visitas = 0
    canal_visitas = []
    canal_visitas.clear()
    for search_result_videos in search_response_videos.get("items",[]):
        # DIVIDE Y FILTRA LAS VIEWS
        if search_result_videos['id']['kind'] == 'youtube#video':
            search_videos = youtube.videos().list(part='statistics', id=search_result_videos['id']['videoId']).execute()
            views = int(search_videos['items'][0]['statistics']['viewCount'])
            idvideo = search_videos['items'][0]['id']
            #GUARDA TOTAL DE VIEWS DEL CANAL
            total_visitas = total_visitas + views
            cantidad_videos+=1
            if cantidad_videos == 1:
                id_video_max = idvideo
                visitas_video_max = views
            if cantidad_videos > 1:
                maximo = max(canal_visitas)
                if maximo < views:
                    id_video_max = idvideo
                    visitas_video_max = views
            # COMPARO MAX Y GUARDO
            canal_visitas.append(views)
    promedio = total_visitas / cantidad_videos
    porcentaje = (visitas_video_max - promedio)/promedio * 100
    canal_porcentajes.append({"video":id_video_max,"porcentaje":porcentaje})
canal_porcentajes.sort(key=lambda x: x['porcentaje'], reverse=True)
primeros_50 = canal_porcentajes[:50]
print(primeros_50)

   


     

            







