import gzip
import filecmp
from time import sleep
from io import StringIO
from pprint import pprint
from bs4 import BeautifulSoup
from urllib.request import urlopen


def download_page(url):
	"""
	Download the page and unzip if needed. Return page data.
	"""
	page = urlopen(url)

	# if gzipped, unzip.
	if page.info().get('Content-Encoding') == 'gzip':
	    buf  = StringIO(page.read())
	    f = gzip.GzipFile(fileobj = buf)
	    return f.read()
	else:
	    return page


def tree_walker(soup, output_file):
	"""
	Walk DOM structure and add nodes to the output file as we go.
	"""
	# TODO: Only add relevant nodes.
	with open(output_file, 'w') as output:
		if soup.name is not None:
			for child in soup.children:
				# add each node to the output file
				output.write(str(child.name) + ":" + str(type(child)) + "\n")
				tree_walker(child, output_file)


def diff_output_files(path1, path2):
	"""
	Diffs output files and returns true if there are differences in the structure.
	"""

	# TODO: better comparison is needed because not all DOM changes are important for us.
	return filecmp.cmp(path1, path2)


def main():

	while True:

		# Scrape first DOM structure.
		orig_data = download_page("http://www.messenger.com/")
		orig_soup = BeautifulSoup(orig_data, "lxml")

		# Walk it and save output to file.
		tree_walker(orig_soup, "output/original_dom_structure.txt")

		print("Sleeping...")
		sleep(20)
		print("Unsleeping...")

		# Scrape second DOM structure.
		updated_data = download_page("http://www.messenger.com/")
		updated_soup = BeautifulSoup(updated_data, "lxml")

		# Walk it and save output to file.
		tree_walker(updated_soup, "output/updated_dom_structure.txt")

		# Diff new version and old version
		file_has_changed = diff_output_files("output/original_dom_structure.txt",
		                                     "output/updated_dom_structure.txt")

		if file_has_changed:
			print("The DOM structure has changed.")
		else:
			print("No changes in the DOM structure yet.")


if __name__ == '__main__':
	main()
