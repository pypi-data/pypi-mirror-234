# djangocms-dag-jetcode

**Django CMS DAG Jetcode** is a plugin for [Django CMS](http://django-cms.org/) that allows you to add [DAG System](https://dag-system.com/)'s Jetcodes on your site.

![preview djangocms-dag-jetcode](https://gitlab.com/kapt/open-source/djangocms-dag-jetcode/-/raw/main/preview.png)

# Requirements

- Python 3.8+
- Django 2.0+
- Django CMS 3.8.0+

# Installation

- run `pip install djangocms-dag-jetcode`
- add `djangocms_dag_jetcode` to your `INSTALLED_APPS`
- include in your `urls.py`
  ```py
  path(
      "djangocms-dag-jetcode/",
      include("djangocms_dag_jetcode.urls", namespace="djangocms-dag-jetcode"),
  ),
  ```
- run `python manage.py migrate djangocms_dag_jetcode`
- import DAG's scripts before the closing `</body>` tag
  ```html
  <script src="https://jetcode.dag-system.com/jetcodes/fr?customerID=<your customer id>" defer></script>
  ```
- add required `<div>` for the basket
  ```html
  <div class="basket-jetcode" data-basket-id="0" css-jetcode-href="https://absolute.path/to/custom.css"></div>
  ```
- add required `<div>` for the popups
  ```html
  <div class="rate-jetcode-def" css-jetcode-href="https://absolute.path/to/custom.css" data-content="jet-code-div"></div>
  <div class="cart-jetcode-def" css-jetcode-href="https://absolute.path/to/custom.css" data-content="jet-code-div"></div>
  <div class="checkout-jetcode-def" css-jetcode-href="https://absolute.path/to/custom.css" data-content="jet-code-div" jetcode-options="zipCode"></div>
  <div class="payinresult-jetcode-def" css-jetcode-href="https://absolute.path/to/custom.css" data-content="jet-code-div"></div>
  ```

You can override some files to customize the style:
- `static/djangocms_dag_jetcode/css/base.css` base style for all Jetcodes
- `static/djangocms_dag_jetcode/css/product.css` product Jetcodes
- `static/djangocms_dag_jetcode/css/productselector.css` product selector Jetcodes
- `static/djangocms_dag_jetcode/css/package.css` package Jetcodes
- `static/djangocms_dag_jetcode/css/container.css` container Jetcodes
- `static/djangocms_dag_jetcode/img/calendar-icon.png` the calendar icon
- `templates/djangocms_dag_jetcode/default.html` the template used to render the Jetcodes

# Settings

## Styles choices

```python
DJANGOCMS_DAG_JETCODE_STYLE_CHOICES = [
  ("my-style", "My custom style"),
]
```
defaults to `[]`

Each style defined in this setting must have a corresponding CSS file in `{STATIC_ROOT}/djangocms_dag_jetcode/css/` (for example: `my-style.css`).

## Cache timeout

Set the cache timeout for the `get_css` view.
```python
DJANGOCMS_DAG_JETCODE_CACHE_TIMEOUT = 15 * 60
```
defaults to `15 * 60` (15 minutes)

When `DEBUG=True`, you can set this setting to `0` to disable the cache.

# Reload Jetcode after CMS plugin edit

When you add or edit a plugin, the CMS does not reload the entire page. You should re-instantiate the Jetcodes to display them without a page refresh. Add this code to your pages:
```js
if (window.hasOwnProperty('CMS') === true) {
  CMS.$(window).on('cms-content-refresh', function () {
    initJetcode()
  })
}
```
