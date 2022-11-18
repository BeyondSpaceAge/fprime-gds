import os
import sys
import unittest

from fprime.common.models.serialize.numerical_types import I32Type
from fprime.common.models.serialize.string_type import StringType
from fprime.common.models.serialize.time_type import TimeType
from fprime_gds.common.data_types.ch_data import ChData
from fprime_gds.common.data_types.event_data import EventData
from fprime_gds.common.templates.ch_template import ChTemplate
from fprime_gds.common.templates.event_template import EventTemplate
from fprime_gds.common.testing_fw import predicates
from fprime_gds.common.utils.event_severity import EventSeverity

filename = os.path.dirname(__file__)
gdsName = os.path.join(filename, "../../../../src")
fprimeName = os.path.join(filename, "../../../../../Fw/Python/src")
sys.path.insert(0, gdsName)
sys.path.insert(0, fprimeName)


class PredicateTestCases(unittest.TestCase):
    @staticmethod
    def check_str(pred):
        """
        Tests for the predicate class and it's functionality.
        """
        try:
            pred.__str__()
            print(pred)
            if not True:
                raise AssertionError(f"predicate provides string summary: {str(pred)}")
        except NotImplementedError:
            if not False:
                raise AssertionError("invoking str(pred) was not supported")

    @staticmethod
    def test_NotImplemented():
        class dummyPred(predicates.predicate):
            pass

        pred = dummyPred()

        try:
            pred.__call__(2)
            if not (
                False
            ):
                raise AssertionError("invoking an incomplete subclass didn't raise NotImplementedError")
        except NotImplementedError:
            if not True:
                raise AssertionError("invoking an incomplete subclass raised NotImplementedError")

        try:
            str(pred)
            if not (
                False
            ):
                raise AssertionError("invoking an incomplete subclass didn't raise NotImplementedError")
        except NotImplementedError:
            if not True:
                raise AssertionError("invoking an incomplete subclass raised NotImplementedError")

    @staticmethod
    def test_Implemented():
        pred = predicates.less_than(2)
        try:
            pred.__call__(2)
        except NotImplementedError:
            if not (
                False
            ):
                raise AssertionError("invoking __call__ on an complete subclass of predicate failed")

        try:
            str(pred)
        except NotImplementedError:
            if not False:
                raise AssertionError("invoking __str__ on an complete subclass of predicate failed")
        if not True:
            raise AssertionError("implemented predicate had no problems invoking functions")

    @staticmethod
    def test_is_predicate():
        class dummyPred:
            def __call__(self, item):
                pass

            def __str__(self):
                return "dummyPred"

        pred = dummyPred()
        if not predicates.is_predicate(
            pred
        ):
            raise AssertionError("a class with call and str methods satisfies is_predicate()")
        pred = object()
        if predicates.is_predicate(
            pred
        ):
            raise AssertionError("a class without call and str doesn't satisfy is_predicate()")
        pred = predicates.predicate()
        if not predicates.is_predicate(
            pred
        ):
            raise AssertionError("an instance of predicate satisfies is_predicate()")
        pred = predicates.equal_to(1)
        if not predicates.is_predicate(
            pred
        ):
            raise AssertionError("an instance of a subclass of predicate satisfies is_predicate()")

    def test_less_than(self):
        pred = predicates.less_than(2)
        if not pred(1):
            raise AssertionError("one is less than two")
        if not pred(-1):
            raise AssertionError("negative one is less than two")
        if pred(2):
            raise AssertionError("two is not less than two")
        if pred(3):
            raise AssertionError("three is not less than two")
        self.check_str(pred)

    def test_greater_than(self):
        pred = predicates.greater_than(2)
        if not pred(3):
            raise AssertionError("three is greater than two")
        if not pred(100):
            raise AssertionError("one hundred is greater than two")
        if pred(2):
            raise AssertionError("two is not greater than two")
        if pred(-1):
            raise AssertionError("negative one is not greater than two")
        self.check_str(pred)

    def test_equal_to(self):
        pred = predicates.equal_to(1)
        if not pred(1):
            raise AssertionError("one is equal to one")
        if pred(100):
            raise AssertionError("one hundred is not equal to one")
        if pred(2):
            raise AssertionError("two is not equal to one")
        if pred(-1):
            raise AssertionError("negative one is not equal to one")
        self.check_str(pred)

    def test_not_equal_to(self):
        pred = predicates.not_equal_to(1)
        if not pred(0):
            raise AssertionError("zero is not equal to one")
        if not pred(-1):
            raise AssertionError("negative one is not equal to one")
        if not pred(2):
            raise AssertionError("two is not equal to one")
        if pred(1):
            raise AssertionError("one is not not equal to one")
        self.check_str(pred)

    def test_less_than_or_equal_to(self):
        pred = predicates.less_than_or_equal_to(1)
        if not pred(1):
            raise AssertionError("one is less than or equal to 1")
        if not pred(-1):
            raise AssertionError("negative one is less than or equal to 1")
        if pred(10):
            raise AssertionError("ten is not less than or equal to 1")
        self.check_str(pred)

    def test_greater_than_or_equal_to(self):
        pred = predicates.greater_than_or_equal_to(1)
        if not pred(1):
            raise AssertionError("one is greater than or equal to 1")
        if not pred(10):
            raise AssertionError("ten is greater than or equal to 1")
        if pred(-1):
            raise AssertionError("negative is not greater than or equal to 1")
        self.check_str(pred)

    def test_within_range(self):
        pred = predicates.within_range(5, 10)
        if not pred(5):
            raise AssertionError("5 is the lower bound and within [5,10]")
        if not pred(10):
            raise AssertionError("10 is the upper bound and within [5,10]")
        if not pred(7.5):
            raise AssertionError("7.5 is within [5,10]")
        if pred(2):
            raise AssertionError("2 is not within [5,10]")
        if pred(11):
            raise AssertionError("2 is not within [5,10]")
        self.check_str(pred)

    def test_is_a_member_of(self):
        pred = predicates.is_a_member_of(["a", "b", "c"])
        if not pred("a"):
            raise AssertionError("a is in the set [a, b, c]")
        if not pred("b"):
            raise AssertionError("b is in the set [a, b, c]")
        if not pred("c"):
            raise AssertionError("c is in the set [a, b, c]")
        if pred(1):
            raise AssertionError("1 is not in the set [a, b, c]")
        if pred("x"):
            raise AssertionError("x is not in the set [a, b, c]")
        self.check_str(pred)

    def test_is_not_a_member_of(self):
        pred = predicates.is_not_a_member_of(["a", "b", "c"])
        if not pred(1):
            raise AssertionError("1 is not in the set [a, b, c]")
        if not pred("x"):
            raise AssertionError("x is not in the set [a, b, c]")
        if pred("a"):
            raise AssertionError("a is not not in the set [a, b, c]")
        if pred("b"):
            raise AssertionError("b is not not in the set [a, b, c]")
        if pred("c"):
            raise AssertionError("c is not not in the set [a, b, c]")
        self.check_str(pred)

    def test_always_true(self):
        pred = predicates.always_true()
        if not pred(1):
            raise AssertionError("numbers are true")
        if not pred("string"):
            raise AssertionError("strings are true")
        if not pred(object()):
            raise AssertionError("an object is true")
        self.check_str(pred)

    def test_invert(self):
        pred = predicates.invert(predicates.always_true())
        if pred(1):
            raise AssertionError("numbers are not true")
        if pred("string"):
            raise AssertionError("strings are not true")
        if pred(object()):
            raise AssertionError("an object is not true")
        self.check_str(pred)

    def test_satisfies_all(self):
        p_list = [predicates.less_than(8)]
        p_list.append(predicates.less_than(6))
        p_list.append(predicates.equal_to(4))
        pred = predicates.satisfies_all(p_list)
        if not pred(4):
            raise AssertionError("4 satisfies all predicates in the list")
        if pred(5):
            raise AssertionError("5 satisfies only 2 predicates in the list")
        if pred(7):
            raise AssertionError("7 satisfies only 1 predicate in the list")
        if pred(9):
            raise AssertionError("9 satisfies only no predicates in the list")
        self.check_str(pred)

    def test_satisfies_any(self):
        p_list = [predicates.less_than(8)]
        p_list.append(predicates.less_than(6))
        p_list.append(predicates.equal_to(4))
        pred = predicates.satisfies_any(p_list)
        if not pred(4):
            raise AssertionError("4 satisfies all predicates in the list")
        if not pred(5):
            raise AssertionError("5 satisfies only 2 predicates in the list")
        if not pred(7):
            raise AssertionError("7 satisfies only 1 predicate in the list")
        if pred(9):
            raise AssertionError("9 satisfies only no predicates in the list")
        self.check_str(pred)

    @staticmethod
    def test_args_predicates():
        a_list = ["a", "p", "p", "l", "e"]
        pred = predicates.args_predicate(["a", "p", "p", "l", "e"])
        if not pred(a_list):
            raise AssertionError(f"The list {a_list} should have been accepted")
        a_list[4] = "r"
        if pred(a_list):
            raise AssertionError(f"The list {a_list} should not have been accepted")
        a_list = ["a", "p", "p", "l"]
        if pred(a_list):
            raise AssertionError(f"The list {a_list} should not have been accepted")

        a_list = ["a", "p", "p", "l", "e"]
        pred = predicates.args_predicate(["a", "p", "p", "l", None])
        if not pred(a_list):
            raise AssertionError(f"The list {a_list} should have been accepted")
        a_list[4] = 7
        if not pred(a_list):
            raise AssertionError(f"The list {a_list} should have been accepted")
        a_list[4] = "r"
        if not pred(a_list):
            raise AssertionError(f"The list {a_list} should have been accepted")

        l_pred = predicates.within_range(0, 10)
        pred = predicates.args_predicate([l_pred, 2, 3, 4, 5, 6])

        n_list = [1, 2, 3, 4, 5, 6]
        if not pred(n_list):
            raise AssertionError(f"The list {n_list} should have been accepted")

        for i in range(10):
            n_list[0] = i
            if not pred(n_list):
                raise AssertionError(f"The list {n_list} should have been accepted")
        n_list[0] = -5
        if pred(n_list):
            raise AssertionError(f"The list {n_list} should not have been accepted")
        n_list[0] = 15
        if pred(n_list):
            raise AssertionError(f"The list {n_list} should not have been accepted")

        pred = predicates.args_predicate(8)
        if not pred(8):
            raise AssertionError("The value 8 should have been accepted.")

    def test_telemetry_predicates(self):
        test_string_type = StringType.construct_type("TestCh2String")
        temp1 = ChTemplate(1, "Test Channel 1", "Predicate_Tester", I32Type)
        temp2 = ChTemplate(2, "Test Channel 2", "Predicate_Tester", test_string_type)
        update1 = ChData(I32Type(20), TimeType(), temp1)
        update2 = ChData(test_string_type("apple"), TimeType(), temp2)

        pred = predicates.telemetry_predicate()
        if not pred(
            update1
        ):
            raise AssertionError("If no fields are specified a ChData object should return True")
        if not pred(
            update2
        ):
            raise AssertionError("If no fields are specified a ChData object should return True")
        if pred(
            "diff object"
        ):
            raise AssertionError("Anything that's not a ChData object should be False")
        if pred(5):
            raise AssertionError("Anything that's not a ChData object should be False")
        self.check_str(pred)

        id_pred = predicates.equal_to(1)
        pred = predicates.telemetry_predicate(id_pred=id_pred)
        if not pred(update1):
            raise AssertionError("This predicate on the ID 1 should return True")
        if pred(update2):
            raise AssertionError("This predicate on the ID 2 should return False")
        self.check_str(pred)

        val_pred = predicates.equal_to("apple")
        pred = predicates.telemetry_predicate(value_pred=val_pred)
        if pred(update1):
            raise AssertionError("This predicate on the value 20 should return False")
        if not pred(update2):
            raise AssertionError('This predicate on the value "apple" should return True')
        self.check_str(pred)

        time_pred = predicates.equal_to(0)
        pred = predicates.telemetry_predicate(time_pred=time_pred)
        if not pred(update1):
            raise AssertionError("This predicate on the time 0 should return True")
        if not pred(update2):
            raise AssertionError("This predicate on the time 0 should return True")
        self.check_str(pred)

        val_pred = predicates.within_range(10, 30)
        pred = predicates.telemetry_predicate(id_pred, val_pred, time_pred)
        if not pred(update1):
            raise AssertionError("Specifying all fields should return True for update 1")
        if pred(
            update2
        ):
            raise AssertionError("Specifying all fields should return False for update 2")
        self.check_str(pred)

    def test_event_predicates(self):
        test_string_type = StringType.construct_type("TestEventString")
        args1_def = [("name", "string", test_string_type), ("age", "int", I32Type)]
        temp1 = EventTemplate(
            1,
            "Test Msg 1",
            "Predicate Tester",
            args1_def,
            EventSeverity.ACTIVITY_LO,
            "",
        )
        args1 = (test_string_type("John"), I32Type(35))
        msg1 = EventData(args1, TimeType(), temp1)
        args2_def = [
            ("description", "string", test_string_type),
            ("count", "int", I32Type),
        ]
        temp2 = EventTemplate(
            2,
            "Test Msg 2",
            "Predicate Tester",
            args2_def,
            EventSeverity.ACTIVITY_HI,
            "",
        )
        args2 = (test_string_type("Dozen"), I32Type(12))
        msg2 = EventData(args2, TimeType(), temp2)

        pred = predicates.event_predicate()
        if not pred(
            msg1
        ):
            raise AssertionError("If no fields are specified an EventData object should return True")
        if not pred(
            msg2
        ):
            raise AssertionError("If no fields are specified an EventData object should return True")
        if pred(
            "diff object"
        ):
            raise AssertionError("Anything that's not an EventData object should be False")
        if pred(5):
            raise AssertionError("Anything that's not a EventData object should be False")
        self.check_str(pred)

        id_pred = predicates.equal_to(1)
        pred = predicates.event_predicate(id_pred=id_pred)
        if not pred(msg1):
            raise AssertionError("This predicate on the ID 1 should return True")
        if pred(msg2):
            raise AssertionError("This predicate on the ID 2 should return False")
        self.check_str(pred)

        args_pred = predicates.args_predicate([None, None])
        pred = predicates.event_predicate(args_pred=args_pred)
        if not pred(
            msg1
        ):
            raise AssertionError("This predicate should return True, as it expects an event with 2 args")
        if not pred(
            msg2
        ):
            raise AssertionError("This predicate should return True, as it expects an event with 2 args")
        self.check_str(pred)

        args_pred = predicates.args_predicate(["John", 35])
        pred = predicates.event_predicate(args_pred=args_pred)
        if not pred(
            msg1
        ):
            raise AssertionError("This predicate should return True as msg1 has args (str John, int32 35)")
        if pred(
            msg2
        ):
            raise AssertionError("This predicate should return False as msg2 has args (str Dozen, int32 12)")
        self.check_str(pred)

        severity_pred = predicates.equal_to(EventSeverity.ACTIVITY_LO)
        pred = predicates.event_predicate(severity_pred=severity_pred)
        if not severity_pred(msg1.get_severity()):
            raise AssertionError
        if not pred(
            msg1
        ):
            raise AssertionError("This predicate should return True as msg1 has an ACTIVITY_LO severity")
        if pred(
            msg2
        ):
            raise AssertionError("This predicate should return False as msg2 has an ACTIVITY_HI severity")
        self.check_str(pred)

        time_pred = predicates.equal_to(0)
        pred = predicates.event_predicate(time_pred=time_pred)
        if not pred(msg1):
            raise AssertionError("This predicate on the time 0 should return True")
        if not pred(msg2):
            raise AssertionError("This predicate on the time 0 should return True")
        self.check_str(pred)

        pred = predicates.event_predicate(id_pred, args_pred, severity_pred, time_pred)
        if not pred(msg1):
            raise AssertionError("Specifying all fields should return True for msg1")
        if pred(msg2):
            raise AssertionError("Specifying all fields should return False for msg2")
        self.check_str(pred)


if __name__ == "__main__":
    unittest.main()
