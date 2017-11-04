from vector import Vector

a = Vector([1, 1])
b = Vector([3, 3])

# Tests
assert a.scale(2) == Vector([2, 2])


# Playground
print(a.normalized, b.normalized)

print(a * b)
print(a.angle_with(b, radians=False))


a = Vector([1, 2, 3])
print(a)

b = a * 3
print(b)

c = a + b
print(c)

print(c + 1.1)

a = Vector([8.218, -9.341])
b = Vector([-1.129, 2.111])
c = Vector([7.119, 8.215])
d = Vector([-8.223, 0.878])
e = Vector([1.671, -1.012, -0.318])
s = 7.41

print(a + b)
print(c - d)
print(e * s)

a = Vector([-0.221, 7.437])
b = Vector([8.813, -1.331, -6.247])
c = Vector([5.581, -2.136])
d = Vector([1.996, 3.108, -4.554])
print(a.magnitude, b.magnitude)
print(1 / c.magnitude, c.normalized)
print(1 / d.magnitude, d.normalized)

a = Vector([7.887, 4.138])
b = Vector([-8.802, 6.776])
print(a * b)

a = Vector([-5.955, -4.904, -1.874])
b = Vector([-4.496, -8.755, 7.103])
print(a * b)


a = Vector([3.183, -7.627])
b = Vector([-2.668, 5.319])
# print(angle(a, b))

a = Vector([7.35, 0.221, 5.188])
b = Vector([2.751, 8.259, 3.985])
# print(angle(a, b, radians=False))


# parallel and orthogonal
a1 = Vector([-7.579, -7.88])
a2 = Vector([22.737, 23.64])

b1 = Vector([-2.029, 9.97, 4.172])
b2 = Vector([-9.231, -6.639, -7.245])

c1 = Vector([-2.328, -7.284, -1.214])
c2 = Vector([-1.821, 1.072, -2.94])

d1 = Vector([2.118, 4.827])
d2 = Vector([0, 0])

print('Is parallel', a1.is_parallel_with(a2))
print('Is parallel', b1.is_parallel_with(b2))
print('Is parallel', c1.is_parallel_with(c2))
print('Is parallel', d1.is_parallel_with(d2))

print('Is orthogonal', a1.is_orthogonal_with(a2))
print('Is orthogonal', b1.is_orthogonal_with(b2))
print('Is orthogonal', c1.is_orthogonal_with(c2))
print('Is orthogonal', d1.is_orthogonal_with(d2))


# 11 Projection Vectors
v = Vector([3.039, 1.879])
b = Vector([0.825, 2.036])

print(v.component_parallel_to(b))

v = Vector([-9.88, -3.264, -8.159])
b = Vector([-2.155, -9.353, -9.473])

print(v.component_orthogonal_to(b))

v = Vector([3.009, -6.172, 3.692, -2.51])
b = Vector([6.404, -9.144, 2.759, 8.718])

print(v.component_orthogonal_to(b))
print(v.component_parallel_to(b))

