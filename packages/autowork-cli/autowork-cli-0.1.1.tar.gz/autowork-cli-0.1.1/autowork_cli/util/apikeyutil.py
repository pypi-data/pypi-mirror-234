class ApiKeyUtil:
    """API KEY脱敏工具"""

    @staticmethod
    def safe_display(apikey):
        if apikey is None:
            return None

        show = apikey[:6]
        if len(apikey) < 6:
            show = apikey[:1]
        return show + '*' * 10
