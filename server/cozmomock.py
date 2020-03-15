import cozmo
from cozmo.util import degrees, radians, distance_mm, speed_mmps, Position, Pose, Rotation, pose_z_angle, rotation_z_angle
import time
import threading
import math
import quaternion
import json

class CozmoBot:
	def __init__(self, aruco):
		self._wsClient = None
		self._dataPubThread = None
		# Empty object.
		self._robot = type('', (), {})()
		self._robot.pose = pose_z_angle(0, 0, 0, degrees(0))
		self._aruco = aruco

	def start(self, code):
		from ws4py.client.threadedclient import WebSocketClient

		self._wsClient = WebSocketClient('ws://localhost:9090/WsPub')
		self._wsClient.connect()

		self._camClient = WebSocketClient('ws://localhost:9090/camPub')
		self._camClient.connect()

		self._wsClient = WebSocketClient('ws://localhost:9090/WsPub')
		self._wsClient.connect()

		self._consoleClient = WebSocketClient('ws://localhost:9090/consolePub')
		self._consoleClient.connect()

		self._blocksClient = WebSocketClient('ws://localhost:9090/blocksPub')
		self._blocksClient.connect()

		if self._aruco:
			self._dataPubThread = threading.Thread(target=self.feedRobotDataInThread)
			self._dataPubThread.daemon = True
			self._dataPubThread.start()

		bot = self

		import cozmo

		exec(code, locals(), locals())

	def consoleLog(self, msgdata):
		self._consoleClient.send(msgdata)

	def feedRobotDataInThread(self):
		print('Starting data feed')
		while True:
			data = {
				'aruco': self._aruco.getMarkers()
			}
			self._wsClient.send(json.dumps(data))
			# Sleep a while
			time.sleep(0.1)

	def _update3d(self):
		# Feed robot data
		def getData(pose):
			if not pose:
				return {
					'x': 0,
					'y': 0,
					'z': 0,
					'rot': (0, 0, 0, 0)
				}
			pos = pose.position
			rot = pose.rotation.q0_q1_q2_q3
			return {
					'x': pos.x,
					'y': pos.y,
					'z': pos.z,
					'rot': rot
				}

		def getCubeData():
			data = getData(None)
			data['seen'] = False
			data['visible'] = False
			return data

		data = {
			'cozmo': getData(self._robot.pose),
			'cubes': [
				getCubeData(),
				getCubeData(),
				getCubeData()
			]
		}
		self._wsClient.send(json.dumps(data))

	def resetCustomObjects(self):
		pass

	def playAnimation(self, animation):
		pass

	def playEmotion(self, emotion):
		pass

	def lift(self, height):
		pass

	def head(self, angle):
		pass

	def getCubeNumber(self, cube):
		return cozmo.objects.LightCube1Id

	def getCubeSeen(self, cube_num):
		return False

	def getCubeIsVisible(self, cube_num):
		return False

	def getDistanceToCube(self, cube_num):
		return 100000

	def getDistanceBetweenCubes(self, cube1_num, cube2_num):
		return 100000

	def pickupCube(self, cube_num):
		return True

	def placeCubeOnGround(self, cube_num):
		return True

	def placeCubeOnCube(self, other_cube_num):
		return True

	def gotoOrigin(self):
		res = self._robot.go_to_pose(self._origin).wait_for_completed()
		return res.state == cozmo.action.ACTION_SUCCEEDED

	def say(self, text):
		return True

	def enableFreeWill(self, enable):
		return True

	def stop(self):
		pass

	def delay(self, seconds):
		time.sleep(seconds)

	def turn(self, angle):
		'''
		Pretends to take 2 seconds per 180 degrees, with 10 iterations per second.
		'''
		finalAngle = self._robot.pose.rotation.angle_z.degrees + angle
		iterations = abs(int(angle / 180.0 * 2 / 0.1))
		if iterations == 0:
			return
		section = angle / iterations
		for i in range(iterations):
			self._robot.pose._rotation = rotation_z_angle(degrees(self._robot.pose.rotation.angle_z.degrees + section))
			self._update3d()
			time.sleep(0.1)
		self._robot.pose._rotation = rotation_z_angle(degrees(finalAngle))
		self._update3d()

	def turnTowardCube(self, cube_num):
		return True

	def driveDistanceWithSpeed(self, distance, speed):
		finalX = self._robot.pose.position.x + math.cos(self._robot.pose.rotation.angle_z.radians) * distance * 10
		finalY = self._robot.pose.position.y + math.sin(self._robot.pose.rotation.angle_z.radians) * distance * 10
		iterations = abs(int(distance / speed / 0.1))
		sectionX = (finalX - self._robot.pose.position.x) / iterations
		sectionY = (finalY - self._robot.pose.position.y) / iterations
		for i in range(iterations):
			self._robot.pose._position._x = self._robot.pose.position.x + sectionX
			self._robot.pose._position._y = self._robot.pose.position.y + sectionY
			self._update3d()
			time.sleep(0.1)
		self._robot.pose._position._x = finalX
		self._robot.pose._position._y = finalY
		self._update3d()

	def driveWheelsWithSpeed(self, lSpeed, rSpeed):
		pass

	def driveTo(self, x, y):
		distX = x - self._robot.pose.position.x / 10.0
		distY = y - self._robot.pose.position.y / 10.0
		angleRad = math.atan2(distY, distX)
		angleDeg = angleRad * 180 / math.pi
		print(angleDeg)
		self.turn(angleDeg - self._robot.pose.rotation.angle_z.degrees)
		dist = math.sqrt(distX * distX + distY * distY)
		self.driveDistanceWithSpeed(dist, 10)

	def waitForTap(self):
		return cozmo.objects.LightCube1Id

	def addStaticObject(self, model, x1, y1, x2, y2, depth, height):
		data = {
			'addStaticObject': {
				'model': model,
				'x1': x1,
				'y1': y1,
				'x2': x2,
				'y2': y2,
				'depth': depth,
				'height': height
			}
		}
		self._wsClient.send(json.dumps(data))

	def setCubeModel(self, model, num):
		data = {
			'setCubeModel': {
				'model': model,
				'cubeNum': num
			}
		}
		self._wsClient.send(json.dumps(data))

	def highlight(self, block, AtlDebugLevel):
		data = {
			'highlight': block
		}
	#	self._blocksClient.send(json.dumps(data))
		print(block, AtlDebugLevel)
		self._blocksClient.send(block)
		if AtlDebugLevel == 1:
			time.sleep(1)
		if AtlDebugLevel == 2:
			time.sleep(2)
		if AtlDebugLevel == 3:
			time.sleep(5)



	# ATL: Add function for custom Object processing
	#  waitForCustonObject()
	# defineCustomCube(<edge in mm>,
	# defineCustomWall(

	def handle_object_appeared(evt, **kw):
		# This will be called whenever an EvtObjectAppeared is dispatched -
		# whenever an Object comes into view.
		if isinstance(evt.obj, CustomObject):
			print("[Bot] Cozmo started seeing a %s" % str(evt.obj.object_type))

	def handle_object_disappeared(evt, **kw):
		# This will be called whenever an EvtObjectDisappeared is dispatched -
		# whenever an Object goes out of view.
		if isinstance(evt.obj, CustomObject):
			print("[Bot] Cozmo stopped seeing a %s" % str(evt.obj.object_type))

#	def waitForCustonObject(self):
#		print("[Bot] Waiting for Custom Object")
#		return self._robot.world.wait_for(cozmo.objects.EvtObjectTapped, timeout=None).obj

	def defineCustomCube(self, CustomObjectMarker, x, md1, md2 ):
		# Add event handlers for whenever Cozmo sees a new object
		self.add_event_handler(cozmo.objects.EvtObjectAppeared, handle_object_appeared)
		self.add_event_handler(cozmo.objects.EvtObjectDisappeared, handle_object_disappeared)

		# define a unique cube (44mm x 44mm x 44mm) (approximately the same size as a light cube)
		# with a 30mm x 30mm Diamonds2 image on every face
		cube_obj = self.world.define_custom_cube(CustomObjectTypes.CustomType00,
												  CustomObjectMarker,
												  x,
												  md1, md2, True)

		if (cube_obj is not None):
			print("[Bot] Cube object defined successfully! " + cube_obj)
		else:
			print("[Bot] Cube object definition failed!")
			return

		print("Show the " + CustomObjectMarker + " to Cozmo and you will see the related objects "
			  "annotated in Cozmo's view window, you will also see print messages "
			  "everytime a custom object enters or exits Cozmo's view.")
