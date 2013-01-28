import urllib2

PAGES = 41
url_base = 'http://tweetminster.com/mps/page:'
OUTPUT_FILE = 'data.sql'

def store(output, full_name, party, constit, twitter, image):
    preamble = "INSERT INTO website_mp (name, party, constituency, twitter_handle) VALUES ("
    full_name = full_name.strip()
    image_name = full_name.replace(' ', '_')
    #    with open(image_name, 'w') as dest: # save the image
    #        print(image)
    #        print(full_name)
    #        try:
    #            img = urllib2.urlopen(image + '.jpg')
    #        except urllib2.HTTPError:
    #            try:
    #                img = urllib2.urlopen(image + '.jpeg')
    #            except urllib2.HTTPError:
    #                try:
    #                    img = urllib2.urlopen(image + '.png')
    #                except urllib2.HTTPError:
    #                    try:
    #                        img = urllib2.urlopen(image + '.JPG')
    #                    except urllib2.HTTPError:
    #                        img = urllib2.urlopen(image)
    #   img = img.read()
    #   dest.write(img)
    l = [full_name, party, constit, twitter]
    l = list(map(lambda x: "'" + x + "'", l))
    output.write(preamble + ', '.join(l) + ")\n")
    
with open(OUTPUT_FILE, 'w') as f:
    for i in range(1, PAGES):
        print(i)
        url = url_base + str(i)
        page = urllib2.urlopen(url)
        source = page.read() 
        source = source.split('section>')[1]
        source = source.split('<div class="tweeters">')[1:]
        for politician in source:
            constit = politician.split('h3')[1][1:-2]
            image = politician.split('src="')[1]
            image = image.split('_normal')[0]
            politician = politician.split('tweetersModuleCopyLeftside')[2]
            politician = politician.split('\n\t\t\t\t')
            twitter = politician[2].split('\t\t\t')[0]
            name = politician[1].split('<br/>')[0]
            party = politician[1].split('class="party">')[1].split('</span>')[0]
            store(f, name, party, constit, twitter, image)
