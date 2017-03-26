import numpy
import math
from enum import Enum

GRID_SIZE = 8
BUFFER_SIZE = 7
TRIGGER_INDEX = BUFFER_SIZE / 2
TRIGGER_COL_IN = 2
TRIGGER_COL_OUT = 5

TRIGGER_THRESHOLD = 10
MAX_THRESHOLD = 3

class Direction(Enum):
	IN = 0
	OUT = 1

class PeopleCounter():
	def __init__(self):
		self.frame_buffer = []
		self.in_count = 0
		self.out_count = 0

	def determine_direction(self, frame, trigger_col):		
		check_col = trigger_col + 1

		current_max = frame[:, trigger_col].max()

		if current_max >= TRIGGER_THRESHOLD:
			# Check for OUT
			for i in range(1,2):  # Look into the past
				past_frame = self.frame_buffer[TRIGGER_INDEX - i]
				# Check for IN
				past_max = past_frame[:, check_col].max()
				if math.fabs(past_max - current_max) <= MAX_THRESHOLD:
					return Direction.OUT

			# Check for IN
			for i in range(1,2):  # Look into the future
				future_frame = self.frame_buffer[TRIGGER_INDEX + i]
				# Check for IN
				future_max = future_frame[:, check_col].max()
				if math.fabs(future_max - current_max) <= MAX_THRESHOLD:
					return Direction.IN
		return None

	def count_people(self, processed_frame):
		# Add frame to buffer and cap buffer at BUFFER_SIZE
		self.frame_buffer.append(processed_frame)
		if len(self.frame_buffer) > BUFFER_SIZE:
			self.frame_buffer.pop(0)

		if len(self.frame_buffer) < BUFFER_SIZE:
			return (0,0)

		current_frame = self.frame_buffer[TRIGGER_INDEX]
		# Process middle frame and check trigger column
		in_trig_dir = self.determine_direction(current_frame, TRIGGER_COL_IN)
		out_trig_dir = self.determine_direction(current_frame, TRIGGER_COL_OUT)

		if in_trig_dir == Direction.IN:
			self.in_count += 0.5
		elif in_trig_dir == Direction.OUT:
			self.out_count += 0.5

		if out_trig_dir == Direction.IN:
			self.in_count += 0.5
		elif out_trig_dir == Direction.OUT:
			self.out_count += 0.5

		return (self.in_count, self.out_count)



