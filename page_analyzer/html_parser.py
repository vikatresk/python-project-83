from bs4 import BeautifulSoup


def truncate(text):
    return f'{text[:255]}...' if len(text) > 255 else text


def parse_page(content):
    soup = BeautifulSoup(content, 'html.parser')

    h1_tag = soup.find('h1')
    h1_content = h1_tag.text if h1_tag else None

    title_tag = soup.title
    title_text = title_tag.text if title_tag else None

    description_tag = soup.find('meta', attrs={'name': 'description'})
    description_content = description_tag['content'] \
        if description_tag else None

    return h1_content, title_text, description_content
