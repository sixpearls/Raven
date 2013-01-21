from django.db import models

# Game, Card, and Token represent what is possible in a game
class Game(models.Model):
  """
  Game represents a collection of cards and tokens that you can play with.

  Need to think about a way to represent a "game setup"-- either Stacks
  pre-filled and/or ways to automate filling initial Stacks.

  Automation: some model that looks like "TableActions" but creates a template. 
  So TA's need to be well designed. Maybe also have templated dependent on # players?
  Too much logic --> not in DB, should be a python script or something

  Also limit (or suggest limits) to what stacks are available and/or where stacks can be expanded into?


  examples: 
  
  Poker "setup" would just be the 52 Cards in a single stack, shuffled. Distribute starting
  chips (tokens) to each player.

  Netrunner "setup" would help you choose (or build) your starting deck
  and then help create the initial stacks (servers for corp, tools for hacker, etc).

  Bohnanza "setup" would automate discarding (into "box" stack) appropriate cards for # of
  players, deal initial hands, etc.

  """
  name = models.CharField(max_length=50)
  description = models.TextField()

  min_players = models.IntegerField()
  max_players = models.IntegerField()

  card_back_text_default = models.TextField()
  card_back_image_default = models.ImageField(upload_to='card_default/') # change this to a function returning game name

class Card(models.Model):
  """
  Card describes a card available in game
  """
  name = models.CharField(max_length=100)
  description = models.TextField()
  game = models.ForeignKey(Game,related_name="cards")
  number = models.IntegerField()

  front_text = models.TextField()
  back_text = models.TextField()

  front_image = models.ImageField(upload_to='card/')
  back_image = models.ImageField(upload_to='card/')

class Token(models.Model):
  """
  Token describes a token available in game
  """
  name = models.CharField(max_length=100)
  description = models.TextField()
  game = models.ForeignKey(Game)
  image = models.ImageField(upload_to='card/')

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
  player = models.ForeignKey('auth.User')
  # may need to switch this so it can beither a user or a session... maybe session
  # already has an optional user?

class TableAction(models.Model):
  """
  Logging for table actions - maybe just lits Manager Functions?
  """
  ACTION_CHOICES = (
    (1, 'move_card'),
    (1, 'move_card'),
    )
  table = models.ForeignKey(Table)
  player = models.ForeignKey('auth.User')
  cards = models.ForeignKey('StackCard') 
  # moving multiple cards generates multiple actions?
  old_stack = models.ForeignKey('Stack',blank=True,null=True,related_name='direct_actions')
  new_stack = models.ForeignKey('Stack',blank=True,null=True,related_name='indirect_actions')
  action = models.IntegerField(choices=ACTION_CHOICES)

class CardMetaMixin(models.Model):
  """
  The physical representation of card(s) while playing the game
  """
  HORIZONTAL = 'h'
  VERTICAL = 'v'
  ORIENTATION_CHOICES = (
    (HORIZONTAL, 'horizontal'),
    (VERTICAL, 'vertical'),
  )

  UP = 'u'
  DOWN = 'd'
  FACING_CHOICES = (
    (UP, 'up'),
    (DOWN, 'down'),
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
  name = models.CharField(blank=True,max_length=100)
  player = models.ForeignKey('auth.User', blank=True, null=True) 
  # which player owns the stack, if any. could be used for hand and player space.
  # null --> central player area.
  is_hand = models.BooleanField(default=False) 
  # if it's a "hand" stack, cards are face up to the player that owns the stack
  # and "face down" to those who are away

  # some kind of physical position? relative to the "table."
  column = models.IntegerField()
  row = models.IntegerField()

  # flags for available operations? operations should probably end up in the StackCard manager
  # shuffle, move from top, move from bottom, move random?, move specific
  # change card orientation, change card facing/direction (any picked), look at all cards,
  # optional: look at face up cards? This could just be in the UI, and not get recorded

class StackCardMetaClass(models.base.ModelBase):
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
  # allow facing and orientation to be blank... might be "better" to have the parent 
  # class allow blanks, and have "Stack"s clean require a value. http://stackoverflow.com/a/8523024/854909
  stack = models.ForeignKey(Stack, related_name="cards")
  card = models.ForeignKey(Card)
  order = models.IntegerField()
  # Should we have some kind of stack of stacks? The only example I can think of
  # is for the corp's "servers" in Netrunner.



