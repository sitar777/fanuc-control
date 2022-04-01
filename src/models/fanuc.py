import sys

from pydantic import BaseModel, validator, root_validator


def validate_float_value(value, min, max):
    value = round(value, 3)
    if value < min and value > max:
        raise ValueError('Value exceeds boundaries')
    return value


class FanucPointDelta(BaseModel):
    dx: float
    dy: float
    dz: float
    dw: float
    dp: float
    dr: float


class FanucPoint(BaseModel):
    x: float
    y: float
    z: float
    w: float
    p: float
    r: float

    @root_validator
    def validate_point(cls, values):
        values['x'] = validate_float_value(values['x'], .01, sys.float_info.max)
        values['y'] = validate_float_value(values['y'], .01, sys.float_info.max)
        values['z'] = validate_float_value(values['z'], .01, 1240)
        values['w'] = validate_float_value(values['w'], -180, 180)
        values['p'] = validate_float_value(values['p'], -180, 180)
        values['r'] = validate_float_value(values['r'], -180, 180)

        return values

    def point_from_delta(self, delta):
        new_point = FanucPoint(
            x=self.x + delta.dx,
            y=self.y + delta.dy,
            z=self.z + delta.dz,
            w=self.w + delta.dw,
            p=self.p + delta.dp,
            r=self.r + delta.dr,
        )
        return new_point


class FanucMessage(BaseModel):
    point: FanucPoint
    velocity: int = 200

    @validator('velocity')
    def validate_velocity(cls, v):
        if v < 0 and v > 2000:
            raise ValueError('Velocity exceeds boundaries')
        return v

    @property
    def bytes(self):
        return b'%d %d %d %d %d %d %d 1' % (
            self.point.x * 1000,
            self.point.y * 1000,
            self.point.z * 1000,
            self.point.w * 1000,
            self.point.p * 1000,
            self.point.r * 1000,
            self.velocity,
        )


if __name__ == '__main__':
    # point 0.1 0.1 0.1 0.1 0.1 0.1 with velocity 200 mm/sec

    point = FanucPoint(
        x=0.1,
        y=0.1,
        z=0.1,
        w=0.1,
        p=0.1,
        r=0.1,
    )

    msg = FanucMessage(point=point, velocity=200)
    assert msg.bytes == b'100 100 100 100 100 100 200 1'
