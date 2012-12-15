from django.db import models

# Game, Card, and Token represent what is possible in a game
class Game(models.Model):
  """
  Game represents a collection of cards and tokens that you can play with.

  Need to think about a way to represent a "game setup"-- either Stacks
  pre-filled and/or ways to automate filling initial Stacks.
  examples: 
  
  Poker "setup" would just be the 52 Cards in a single stack, shuffled.

  Netrunner "setup" would help you choose (or build) your starting deck
  and then help create the initial stacks.
  """
  name = models.CharField()
  description = models.TextField()

  min_players = models.IntegerField()
  max_players = models.IntegerField()

  card_back_text_default = models.TextField()
  card_back_image_default = models.ImageField()
  #

class Card(models.Model):
  """
  Card describes a card available in game
  """
  name = models.CharField()
  description = models.TextField()
  game = models.ForeignKey(Game)

  front_text = models.TextField()
  back_text = models.TextField()

  front_image = models.ImageField()
  back_image = models.ImageField()

class Token(models.Model):
  """
  Token describes a token available in game
  """
  name = models.CharField()
  description = models.TextField()
  game = models.ForeignKey(Game)
  image = models.ImageField()

class Table(models.Model):
  """
  Where one plays a game
  """
  game = models.ForeignKey(Game)

class TablePlayers(models.Model):
  """
  Relate users and table
  """
  table = models.ForeignKey(Table)
  players = models.ForeignKey('auth.User')

class CardMetaMixin(models.Model):
  """
  The physical representation of card(s) while playing the game
  """
  HORIZONTAL = 'h'
  VERTICAL = 'v'
  ORIENTATION_CHOICES = (
    ('h', 'horizontal'),
    ('v', 'vertical'),
  )

  UP = 'u'
  DOWN = 'd'
  FACING_CHOICES = (
    ('u', 'up'),
    ('d', 'down'),
  )

  orientation = models.CharField(max_length=1,choices=ORIENTATION_CHOICES,default=VERTICAL)
  facing = models.CharField(max_length=1,choices=FACING_CHOICES,default=UP)
  table = models.ForeignKey(Table)
  tokens = models.ManyToManyField(Token) # a card or stack can have a token(s) placed

  class Meta:
    abstract = True

class Stack(CardMetaMixin):
  """
  While playing, cards belong in Stacks. Provides default positioning for the stack.
  """
  name = models.CharField()
  player = models.ForeignKey('auth.User') # which player owns the stack, if any
  is_hand = models.BooleanField() 
  # if it's a "hand" stack, cards are face up to the player that owns the stack
  # and face_down if it's away

  # some kind of physical position? relative to the "table."   
  column = models.IntegerField()
  row = models.IntegerField()

class StackCardMetaClass(model.ModelBase):
  def __new__(cls, name, bases, attrs):
      this = super(StackCardMetaClass, cls).__new__(cls, name, bases, attrs)
      this._meta.get_field('facing').blank = True 
      this._meta.get_field('orientation').blank = True
      return this

class StackCard(CardMetaMixin):
  """
  Relate Cards and Stacks. Provides individual positioning, order.
  """
  __metaclass__ = StackCardMetaClass
  stack = models.ForeignKey(Stack)
  card = models.ForeignKey(Card)
  order = models.IntegerField()



