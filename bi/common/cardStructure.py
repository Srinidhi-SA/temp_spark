# -*- coding: utf-8 -*-
"""
This module contains Card Structure for Narratives
"""

class NarrativesTree:
    """
    Functionalities:

    add single node => add_a_node
    add multiple node => add_nodes
    add single card => add_a_card
    add multiple card => add_cards
    set name => set_name
    get name => get_name
    """

    def __init__(self,name=None, slug=None, listOfNodes=[], listOfCards=[]):
        self.name = str(name)
        self.slug = str(slug)
        self.listOfNodes = list(listOfNodes)
        self.listOfCards = list(listOfCards)

    def set_name(self,name):
        self.name = str(name)

    def add_a_node(self,newNode):
        self.listOfNodes.append(newNode)

    def add_nodes(self,nodeList):
        self.listOfNodes += nodeList

    def add_a_card(self,newCard):
        self.listOfCards.append(newCard)

    def add_cards(self,cardList):
        self.listOfCards += cardList

    def get_name(self):
        return self.name

    def get_all_cards(self):
        return self.listOfCards

    def get_all_nodes(self):
        return self.listOfNodes

    def get_card_count(self):
        return len(self.listOfCards)

    def get_node_count(self):
        return len(self.listOfNodes)


class NormalCard:
    """
    Defines the structure for a normal Card
    cardData is always an array of HtmlData or C3ChartData
    """

    def __init__(self,name=None,slug=None,cardData = []):
        self.cardType = "normal"
        self.name = name
        self.slug = slug
        self.cardData = cardData

    def set_card_data(self,data):
        self.cardData = data

    def set_card_name(self,name):
        self.name = name

    def insert_card_data(self,idx,data):
        self.cardData.insert(idx,data)

    def get_card_data(self):
        return self.cardData

    def get_card_name(self):
        return self.name

    def get_card_type(self):
        return self.cardType

class SummaryCard:
    """
    Defines the structure for a Summary Card
    cardData is always an array of HtmlData or C3ChartData
    """

    def __init__(self,name=None,slug=None,cardData = {}):
        self.cardType = "summary"
        self.name = name
        self.slug = slug
        self.cardData = cardData

    def set_card_data(self,data):
        self.cardData = data

    def set_card_name(self,name):
        self.name = name

    def insert_card_data(self,idx,data):
        self.cardData.insert(idx,data)

    def get_card_data(self):
        return self.cardData

    def get_card_name(self):
        return self.name

    def get_card_type(self):
        return self.cardType

class HtmlData:

    def __init__(self,data=None):
        self.dataType = "html"
        self.data = data

    def set_data(self,data):
        self.data = data

    def get_data(self):
        return self.data

    def get_data_type(self):
        return self.dataType


class C3ChartData:

    def __init__(self,data=None):
        self.dataType = "c3Chart"
        self.data = data

    def set_data(self,data):
        self.data = data

    def get_data(self):
        return self.data

    def get_data_type(self):
        return self.dataType
