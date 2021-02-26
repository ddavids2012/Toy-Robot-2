import unittest
import robot as r
from unittest.mock import patch
from io import StringIO


class TestToy_robot(unittest.TestCase):

    @patch("sys.stdin", StringIO("bot\nbob\n"))
    def test_get_robot_name(self):
        self.assertEqual(r.get_robot_name(), "BOT")
        self.assertEqual(r.get_robot_name(), "BOB")


    def test_output_help_list(self):
        # self.assertTrue(" I can understand these commands:\n")
        self.assertEqual(r.output_help_list(["help", "off","forward","back","right","left","sprint"],
        ["provide information about commands","Shut down robot","move robot forward","move robot backwards","turns robot right","turns robot left","gives robot a short burst of speed extra distance"]),
        "I can understand these commands:\n help - provide information about commands\n off - Shut down robot\n forward - move robot forward\n back - move robot backwards\n right - turns robot right\n left - turns robot left\n sprint - gives robot a short burst of speed extra distance\n")


    def test_change_value_in_tuple(self):
        self.assertEqual(r.change_value_in_tuple((0,0),1,10),(0,10))
        self.assertEqual(r.change_value_in_tuple((0,0),0,10),(10,0))
    
    
    def test_in_limit(self):
        self.assertEqual(r.in_limit(50,0),True)
        self.assertEqual(r.in_limit(100,0),True)
        self.assertEqual(r.in_limit(-100,0),True)
        self.assertEqual(r.in_limit(-50,0),True)
        self.assertEqual(r.in_limit(200,0),False)
        self.assertEqual(r.in_limit(-200,0),False)

        self.assertEqual(r.in_limit(50,1),True)
        self.assertEqual(r.in_limit(100,1),True)
        self.assertEqual(r.in_limit(-100,1),True)
        self.assertEqual(r.in_limit(-50,1),True)
        self.assertEqual(r.in_limit(201,1),False)
        self.assertEqual(r.in_limit(-201,1),False)


    def test_robot_direction(self):
        self.assertEqual(r.robot_direction('right','forward'),'right')
        self.assertEqual(r.robot_direction('right','back'),'left')
        self.assertEqual(r.robot_direction('right','right'),'back')
        self.assertEqual(r.robot_direction('right','left'),'forward')

        self.assertEqual(r.robot_direction('left','forward'),'left')
        self.assertEqual(r.robot_direction('left','back'),'right')
        self.assertEqual(r.robot_direction('left','right'),'forward')
        self.assertEqual(r.robot_direction('left','left'),'back')


    def test_get_move(self):
        self.assertEqual(r.get_move("forward 10",["help", "off","forward","back","right","left","sprint"]),"forward")
        self.assertEqual(r.get_move("back 10",["help", "off","forward","back","right","left","sprint"]),"back")
        self.assertEqual(r.get_move("help",["help", "off","forward","back","right","left","sprint"]),"help")
        self.assertEqual(r.get_move("off",["help", "off","forward","back","right","left","sprint"]),"off")
        self.assertEqual(r.get_move("right",["help", "off","forward","back","right","left","sprint"]),"right")
        self.assertEqual(r.get_move("left",["help", "off","forward","back","right","left","sprint"]),"left")
        self.assertEqual(r.get_move("sprint 10",["help", "off","forward","back","right","left","sprint"]),"sprint")


    def test_get_distance(self):
        self.assertEqual(r.get_distance("forward 10"),"10")

        self.assertEqual(r.get_distance("back 10"),"10")
        self.assertEqual(r.get_distance("right"),"no_steps")
        self.assertEqual(r.get_distance("left"),"no_steps")
        self.assertEqual(r.get_distance("off"),"no_steps")
        self.assertEqual(r.get_distance("help"),"no_steps")
        self.assertEqual(r.get_distance("sprint 10"),"10")


    def test_get_coordinates(self):
        self.assertEqual(r.get_coordinates("forward 10",(0,0),"10","forward"),(0,10))
        self.assertEqual(r.get_coordinates("back 10",(0,0),"10","forward"),(0,-10))
        self.assertEqual(r.get_coordinates("forward 10",(0,0),"10","back"),(0,-10))
        self.assertEqual(r.get_coordinates("back 10",(0,0),"10","back"),(0,-10))
        self.assertEqual(r.get_coordinates("forward 10",(0,0),"10","right"),(10,0))
        self.assertEqual(r.get_coordinates("back 10",(0,0),"10","right"),(-10,0))
        self.assertEqual(r.get_coordinates("forward 10",(0,0),"10","left"),(-10,0))
        self.assertEqual(r.get_coordinates("back 10",(0,0),"10","left"),(10,0))


    def test_calculate_sprint_taken_steps(self):
        self.assertEqual(r.calculate_sprint_taken_steps(5,"bob"),15)
        self.assertEqual(r.calculate_sprint_taken_steps(4,"bob"),10)
        self.assertEqual(r.calculate_sprint_taken_steps(3,"bob"),6)
        

    def test_sprint(self):
        self.assertEqual(r.sprint(5,("bob",(0,0),"forward")),("bob",(0,15),"forward"))
        self.assertEqual(r.sprint(4,("bob",(0,0),"forward")),("bob",(0,10),"forward"))
    

    def test_check_valid_input(self):
        self.assertEqual(r.check_valid_input('forward','10'),('forward','10'))
        self.assertEqual(r.check_valid_input('back','10'),('back','10'))
        self.assertEqual(r.check_valid_input('sprint','5'),('sprint','5'))


    def test_choose_command(self):
        self.assertEqual(r.choose_command("forward 10",["help", "off","forward","back","right","left","sprint"]),("forward","10"))
        self.assertEqual(r.choose_command("back 10",["help", "off","forward","back","right","left","sprint"]),("back","10"))
        self.assertEqual(r.choose_command("sprint 10",["help", "off","forward","back","right","left","sprint"]),("sprint","10"))


    def test_move_robot(self):
        self.assertEqual(r.move_robot("forward","10",("bob",(0,0),"forward")),("bob",(0,10),"forward"))
        self.assertEqual(r.move_robot("forward","10",("bob",(0,0),"right")),("bob",(10,0),"right"))


    def test_do_command(self):
        self.assertEqual(r.do_command(("forward","10"),["help", "off","forward","back","right","left","sprint"],
        ["provide information about commands","Shut down robot","move robot forward","move robot backwards","turns robot right","turns robot left","gives robot a short burst of speed extra distance"],
        ("bob",(0,0),"forward")),("bob",(0,10),"forward"))
        self.assertEqual(r.do_command(("right","0"),["help", "off","forward","back","right","left","sprint"],
        ["provide information about commands","Shut down robot","move robot forward","move robot backwards","turns robot right","turns robot left","gives robot a short burst of speed extra distance"],
        ("bob",(0,0),"forward")),("bob",(0,0),"right"))