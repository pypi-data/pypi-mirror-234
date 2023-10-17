from eveuniverse.models import EveStation

from django.test import TestCase

from allianceauth.eveonline.models import EveCharacter, EveCorporationInfo

from ..models import Agent, LocateChar, LocateCharAgent
from .load_eveuniverse import load_eveuniverse


class TestModels(TestCase):
    def setUp(self):
        load_eveuniverse()
        self.character = EveCharacter.objects.create(
            character_id=1,
            character_name='Test Character',
            corporation_id=1,
            corporation_name='Test Corporation'
        )
        self.corporation = EveCorporationInfo.objects.create(
            corporation_id=1,
            corporation_name='Test Corporation',
            member_count=1
        )
        self.station = EveStation.objects.get(id=60003760)
        self.locate_char = LocateChar.objects.create(
            character=self.character
        )
        self.agent = Agent.objects.create(
            character=EveCharacter.objects.create(character_id=2, character_name='Test Agent', corporation_id=2, corporation_name='Test Agent Corporation'),
            corporation=EveCorporationInfo.objects.create(corporation_id=2,corporation_name='Test Agent Corporation', member_count=2),
            station=EveStation.objects.get(id=60003760),
            level=1,
            type=1,
            is_locator=True
        )

    def test_agent_cooldown(self):
        # Test Agent cooldown property

        self.assertEqual(self.agent.cooldown, 5)
        self.agent.level = 3
        self.assertEqual(self.agent.cooldown, 15)

    def test_locate_char_str(self):
        # Test __str__ method of LocateChar
        self.assertEqual(str(self.locate_char), 'Test Character')

    def test_locate_charagent_str(self):
        # Test __str__ method of LocateCharAgent
        locate_char_agent = LocateCharAgent.objects.create(
            agent=self.agent,
            character=self.character
        )
        self.assertEqual(str(locate_char_agent), 'Test AgentTest Character')
