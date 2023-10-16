from allianceauth import hooks
from allianceauth.theme.hooks import ThemeHook


class BootstrapDarkThemeHook(ThemeHook):
    """
    Bootstrap in all its glory!
    https://getbootstrap.com/
    """

    def __init__(self):
        ThemeHook.__init__(
            self,
            "Bootstrap Dark",
            "Powerful, extensible, and feature-packed frontend toolkit.",
            css=[{
                "url": "https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/css/bootstrap.min.css",
                "integrity": "sha512-t4GWSVZO1eC8BM339Xd7Uphw5s17a86tIZIj8qRxhnKub6WoyhnrxeCIMeAqBPgdZGlCcG2PrZjMc+Wr78+5Xg=="
            }],
            js=[{
                "url": "https://cdnjs.cloudflare.com/ajax/libs/popper.js/2.11.8/umd/popper.min.js",
                "integrity": "sha512-TPh2Oxlg1zp+kz3nFA0C5vVC6leG/6mm1z9+mA81MI5eaUVqasPLO8Cuk4gMF4gUfP5etR73rgU/8PNMsSesoQ=="
            }, {
                "url": "https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/js/bootstrap.min.js",
                "integrity": "sha512-3dZ9wIrMMij8rOH7X3kLfXAzwtcHpuYpEgQg1OA4QAob1e81H8ntUQmQm3pBudqIoySO5j0tHN4ENzA6+n2r4w=="
            }],
            html_tags="data-bs-theme=dark",
            header_padding="3.5em"
        )


@hooks.register('theme_hook')
def register_bootstrap_dark_hook():
    return BootstrapDarkThemeHook()
