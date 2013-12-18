from collections import namedtuple
from math import sqrt
import random,csv,os,argparse,sys
try:
    import Image
except ImportError:
    from PIL import Image


Point = namedtuple('Point', ('coords', 'n', 'ct'))
Cluster = namedtuple('Cluster', ('points', 'center', 'n'))

def get_points(img):
    points = []
    w, h = img.size
    for count, color in img.getcolors(w * h):
        points.append(Point(color, 3, count))
    return points

rtoh = lambda rgb: '#%s' % ''.join(('%02x' % p for p in rgb))

def colorz(filename, n=3):
    img = Image.open(filename)
    img.thumbnail((200, 200))
    w, h = img.size

    points = get_points(img)
    clusters = kmeans(points, n, 1)
    rgbs = [map(int, c.center.coords) for c in clusters]
    return map(rtoh, rgbs)

def euclidean(p1, p2):
    return sqrt(sum([
        (p1.coords[i] - p2.coords[i]) ** 2 for i in range(p1.n)
    ]))

def calculate_center(points, n):
    vals = [0.0 for i in range(n)]
    plen = 0
    for p in points:
        plen += p.ct
        for i in range(n):
            vals[i] += (p.coords[i] * p.ct)
    return Point([(v / plen) for v in vals], n, 1)

def kmeans(points, k, min_diff):
    clusters = [Cluster([p], p, p.n) for p in random.sample(points, k)]

    while 1:
        plists = [[] for i in range(k)]

        for p in points:
            smallest_distance = float('Inf')
            for i in range(k):
                distance = euclidean(p, clusters[i].center)
                if distance < smallest_distance:
                    smallest_distance = distance
                    idx = i
            plists[idx].append(p)

        diff = 0
        for i in range(k):
            old = clusters[i]
            center = calculate_center(plists[i], old.n)
            new = Cluster(plists[i], center, old.n)
            clusters[i] = new
            diff = max(diff, euclidean(old.center, new.center))

        if diff < min_diff:
            break

    return clusters


def main():
    parser = argparse.ArgumentParser(description='Dominatio. Get the dominant color(s) from an image')
    parser.add_argument("-d", "--directory", dest="folder", help="the path to your images folder", required=True)
    parser.add_argument("-o", "--output", dest="output", default="output.tsv", help="the output file (.tsv file)")
    parser.add_argument("-c", "--colorNumber", dest="color_number", default=1, type=int, help="The number of dominant color(s) to calculate. By default just the first one, max 10")
    options = parser.parse_args()

    if options.color_number > 10:
        sys.stdout.write("It seems you want too many colors! I'll calculate max 10 colors :P\n")
        sys.stdout.flush()
        options.color_number = 10

    images = [f for f in os.listdir(options.folder) if os.path.isfile(os.path.join(options.folder,f))]

    writer = csv.writer(open(options.output, 'wb'), delimiter='\t', quotechar='"')
    headers = ['file_name']
    for i in range(options.color_number):
        headers.append('color_' + str(i+1))
    writer.writerow(headers)

    total = len(images)

    for n, image in enumerate(images):
        try:
            row = [image]
            sys.stdout.write('\x1b[2K\r[' + str(n+1) + '/' + str(total) +'] ' + image)
            sys.stdout.flush()
            dominant = colorz(os.path.join(options.folder,image), options.color_number)
            row.extend(dominant)
            writer.writerow(row)
        except:
            sys.stdout.write('\x1b[2K\r[' + str(n+1) + '/' + str(total) +'] ' + "I'm not an image: " + image)
            sys.stdout.flush()
            continue

    sys.stdout.write('\x1b[2K\r')
    sys.stdout.flush()
    sys.exit()

if __name__ == '__main__':
        main()