from django.contrib import admin
from models import Game, Card, Token

class CardAdmin(admin.ModelAdmin):
    pass
admin.site.register(Card, CardAdmin)

class TokenAdmin(admin.ModelAdmin):
    pass
admin.site.register(Token, TokenAdmin)

class GameAdmin(admin.ModelAdmin):
    pass
admin.site.register(Game, GameAdmin)