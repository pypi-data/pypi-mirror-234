from allianceauth import hooks
from allianceauth.theme.hooks import ThemeHook


class DarklyThemeHook(ThemeHook):
    """
    The default auth theme
    https://bootswatch.com/darkly/
    """

    def __init__(self):
        ThemeHook.__init__(
            self,
            "Darkly",
            "Flatly in night mode!",
            css=[{
                "url": "https://cdnjs.cloudflare.com/ajax/libs/bootswatch/5.3.0/darkly/bootstrap.min.css",
                "integrity": "sha512-3xynESL0QF3ERUl9se1VJk043nWT+UzWJveifBw7kLtC226vyGINZFtmyK015F83KBSNW+67alYSY2cCj1LHOQ=="
            }],
            js=[{
                "url": "https://cdnjs.cloudflare.com/ajax/libs/popper.js/2.11.8/umd/popper.min.js",
                "integrity": "sha512-TPh2Oxlg1zp+kz3nFA0C5vVC6leG/6mm1z9+mA81MI5eaUVqasPLO8Cuk4gMF4gUfP5etR73rgU/8PNMsSesoQ=="
            }, {
                "url": "https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/js/bootstrap.min.js",
                "integrity": "sha512-3dZ9wIrMMij8rOH7X3kLfXAzwtcHpuYpEgQg1OA4QAob1e81H8ntUQmQm3pBudqIoySO5j0tHN4ENzA6+n2r4w=="
            }],
            header_padding="4.5em"
        )


@hooks.register('theme_hook')
def register_darkly_hook():
    return DarklyThemeHook()
