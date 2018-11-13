from anime_downloader import get_anime_class

# Both of the below functions return the same class
NineAnime = get_anime_class('9anime')

anime = NineAnime(
            'https://www1.9anime.to/watch/your-name-dub.l4yz/n2qm6m',
            quality='720p')
print(anime.title)

for ep in anime:
    print(ep.ep_no) # int: Episode number of the episode
    print(ep.pretty_title)  # str: title in the format <animename>-<ep_no>
    print(ep.quality)
    print(ep.stream_url)  # stream url for the epiosde.
    print(ep.title)  # title from site. Most probably giberrish

ep = anime[0]
print(dir(ep))
ep.download()  # downloads the episode