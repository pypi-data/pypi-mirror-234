from allianceauth import hooks
from allianceauth.theme.hooks import ThemeHook


class MateriaThemeHook(ThemeHook):
    """
    Materia theme
    https://bootswatch.com/materia/
    """

    def __init__(self):
        ThemeHook.__init__(
            self,
            "Materia",
            "Material is the metaphor",
            css=[{
                "url": "https://cdnjs.cloudflare.com/ajax/libs/bootswatch/5.3.0/materia/bootstrap.min.css",
                "integrity": "sha512-FukZyva60KXjmN0uleimuMCoAUwuRha1fSCdzWtxZ29YBIev3gGBU0FpTIEfmGZ9YSrmgW4Pv5geC/q11RuATg=="
            }],
            js=[{
                "url": "https://cdnjs.cloudflare.com/ajax/libs/popper.js/2.11.8/umd/popper.min.js",
                "integrity": "sha512-TPh2Oxlg1zp+kz3nFA0C5vVC6leG/6mm1z9+mA81MI5eaUVqasPLO8Cuk4gMF4gUfP5etR73rgU/8PNMsSesoQ=="
            }, {
                "url": "https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/js/bootstrap.min.js",
                "integrity": "sha512-3dZ9wIrMMij8rOH7X3kLfXAzwtcHpuYpEgQg1OA4QAob1e81H8ntUQmQm3pBudqIoySO5j0tHN4ENzA6+n2r4w=="
            }],
            header_padding="5.25em"
        )


@hooks.register('theme_hook')
def register_materia_hook():
    return MateriaThemeHook()
