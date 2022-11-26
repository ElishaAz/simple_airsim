from datetime import datetime
class PidController:
    def __init__(self, p=0, i=0, d=0, n=1, invalid=-1):
        self.kP = p
        self.kI = i
        self.kD = d
        self._error_prior = 0
        self._integral_prior = 0
        self.ans = 0
        self.target = n
        self.min = -1000000
        self.max = 1000000
        self.last_time = 0
        self.__derivative_prior = 0  # # for debug only !
        self.dt = 0.1
        self.invalid = -1

    def __str__(self):
        str = f" Ans = {self.ans} ,_integral_prior = {self._integral_prior},_error_prior ={self._error_prior},__derivative_prior = {self.__derivative_prior},time{self.last_time}"
        return str

    def set_bounds(self, min, max):
        self.min = min
        self.max = max

    def reset(self):
        self._error_prior = 0
        self._integral_prior = 0
        self._counter = 0
        self.ans = 0

    def constrain(slef, angel, min, max):
        if angel > max:
            angel = max
        elif angel < min:
            angel = min
        return angel

    def update_dt(self, now):
        dt = now - self.last_time  # get the dt
        self.last_time = now
        self.dt = dt

    def pid(self, curr, now):
        if curr == None or curr == self.invalid or curr < 0:
            return self.ans
        self.update_dt(now)
        error = curr - self.target
        derivative = (error - self._error_prior) / self.dt
        integral = self._integral_prior + error * self.dt

        self._error_prior = error
        self._integral_prior = integral
        self.__derivative_prior = derivative  # for debug only !

        ans = (error * self.kP + derivative * self.kD + integral * self.kI)
        ans = self.constrain(ans, self.min, self.max)
        self.ans = ans
        return ans


