from django.utils.text import slugify
from django.utils.translation import gettext as _

import markdown
from bs4 import BeautifulSoup

CLASS_ADDERS = [
    ("h1", "utrecht-heading-1"),
    ("h2", "utrecht-heading-2"),
    ("h3", "utrecht-heading-3"),
    ("h4", "utrecht-heading-4"),
    ("h5", "utrecht-heading-5"),
    ("h6", "utrecht-heading-6"),
    ("img", "image"),
    ("li", "li"),
    ("p", "p"),
    ("a", "link link--secondary"),
    ("table", "table table--content"),
    ("th", "table__header"),
    ("td", "table__item"),
]


def get_rendered_content(content: str) -> str:
    """
    Takes object's content as an input and returns the rendered one.
    """
    md = markdown.Markdown(extensions=["tables"])
    # remove weird undocumented \\< escape/prefix generated by CKeditor
    content = content.replace("\\<", "<")
    html = md.convert(content)
    soup = BeautifulSoup(html, "html.parser")

    for tag, class_name in CLASS_ADDERS:
        for element in soup.find_all(tag):
            element.attrs["class"] = class_name
            if element.name == "a" and element.attrs.get("href", "").startswith("http"):
                element.attrs["target"] = "_blank"

    return str(soup)


def get_product_rendered_content(product):
    """
    Takes product's content as an input and returns the rendered one.
    """
    md = markdown.Markdown(extensions=["tables"])
    # remove weird undocumented \\< escape/prefix generated by CKeditor
    content = product.content.replace("\\<", "<")
    html = md.convert(content)
    soup = BeautifulSoup(html, "html.parser")

    for tag, class_name in CLASS_ADDERS:
        for element in soup.find_all(tag):
            if element.attrs.get("class") and "cta-button" in element.attrs["class"]:
                continue

            element.attrs["class"] = class_name

            if tag == "h2":
                element.attrs["id"] = f"subheading-{slugify(element.text)}"

            if "[CTABUTTON]" in element.text:
                # decompose the element when product doesn't have either a link or a form
                if not (product.link or product.form):
                    element.decompose()
                    continue

                # icon
                icon = soup.new_tag("span")
                icon.attrs.update(
                    {"aria-label": product.button_text, "class": "material-icons"}
                )
                icon.append("arrow_forward")

                # button
                element.name = "a"
                element.string = ""
                element.attrs.update(
                    {
                        "class": "button button--textless button--icon button--icon-before button--primary cta-button",
                        "href": (product.link if product.link else product.form_link),
                        "title": product.button_text,
                        "aria-label": product.button_text,
                    }
                )
                element.append(icon)
                element.append(product.button_text)

                if product.link:
                    element.attrs.update({"target": "_blank"})

            elif element.name == "a" and element.attrs.get("href", "").startswith(
                "http"
            ):
                icon = soup.new_tag("span")
                icon.attrs.update(
                    {
                        "aria-hidden": "true",
                        "aria-label": _("Opens in new window"),
                        "class": "material-icons",
                    }
                )
                icon.append("open_in_new")
                element.append(icon)

    return soup
