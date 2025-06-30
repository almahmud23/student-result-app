class Student:
    def __init__(self, name, roll, marks):
        self.name = name
        self.roll = roll
        self.marks = marks

    def average(self):
        return sum(self.marks) / len(self.marks)

    def grade(self):
        if any(mark < 33 for mark in self.marks):
            return "Fail"
        avg = self.average()
        return (
            "A+" if avg >= 90 else
            "A" if avg >= 80 else
            "B" if avg >= 70 else
            "C" if avg >= 60 else
            "Fail"
        )


class SpecialStudent(Student):
    def __init__(self, name, roll, marks, bonus=5):
        super().__init__(name, roll, marks)
        self.bonus = bonus

    def average(self):
        return min(super().average() + self.bonus, 100)

    def grade(self):
        if any(mark < 33 for mark in self.marks):
            if self.average() >= 40:
                return "Pass & C"
            else:
                return "Fail"
        return super().grade()
