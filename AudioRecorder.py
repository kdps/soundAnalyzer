
import time, sys
import pymedia.audio.sound as sound
import pymedia.audio.acodec as acodec

from scipy import *
import wave

# takes sound in Hz and returns a string with the name of the closest note
def find_closest_note(sound):
	dist = 
	result = ""
	for i in notes.keys():
		newDist = abs(sound-i)
		if newDist<dist:
			dist = newDist
			result = notes[i]
	return result
   
notes = dict({:"(LOW)",.:"C",.:"C#",.:"D",.:"D#",.:"E",.:"F",.:"F#",:"G",.:"G#",:"A",.:"A#",.:"B",.:"C",.:"C#",.:"D",.:"D#",.:"E",.:"F",:"F#",:"G",.:"G#",:"A",.:"A#",.:"B",.:"C",.:"C#",.:"D",.:"D#",.:"E",.:"F",.:"F#",:"G",.:"G#",:"A",.:"A#",.:"B",.:"C",.:"C#",.:"D",.:"D#",.:"E",.:"F",.:"F#",.:"G",.:"G#",:"A",.:"A#",.:"B",.:"C",.:"C#",.:"D",.:"D#",.:"E",:"(HIGH)"})

time_to_record =  # seconds. also read from input. only relevant if from_mic=True
sample_rate =  # samples per second
FACTOR = .
number_of_samples_to_process = int(*FACTOR) # ^ to make FFT work fast, and enough time for accurate reading, but not too long so we don't have too much spread
snd = 
from_mic = True # if True, the prog takes input from mic. if False - from file named filename
file_is_over = False # set to True when input file is over.
filename = "../chords/yonatan hakatan.wav"
peaks_only = True #
cur_time = .
cur_sample = 
now_playing = dict()
sound_vector = []
last_processed_time = . # seconds
interval = . # seconds
sound_events = [] # will contain ( time , event_number: =start, =stop , note_index , note_name )

DecaySamplesNeeded =  # this is how many samples in a row are needed to find a decay
DecayFactor = . # how strong should decay be in order to be detected (low = strong decay.  = every decay is detected)
ReplayFactor = . # how strong should re-play be to be detected.  = very weak is detected. . - medium. . - only very aggressive re-play is detected

MinPower = *FACTOR # minimum power to detect note
StopAreaPower = *FACTOR # power below which notes have to go to be stopped
DetectionFrames =  # how many frames should we wait before we put detected notes in the events vector. "waits" to see if this is a real tone or an overtone
StopPower = *FACTOR*

def init():
	global snd
	if(from_mic):
		snd = sound.Input( sample_rate, , sound.AFMT_S_LE )
	else:
		snd = wave.open(filename)
	   
def start_rec():
	if(from_mic):
		snd.start()
	   
def read_data():
	global cur_sample
	global cur_time
	global sound_vector
   
	if(from_mic):
		temp = snd.getData()
	else:
		temp = snd.readframes(  )
		if(len(temp)==):
			global file_is_over
			file_is_over = True
   
	if temp and len( temp ):
		for i in range(, len(temp), ):
			t = ord(temp[i])+*ord(temp[i+])
			if t > :
				t = - + t
			sound_vector.append(t)
			cur_sample += 
		cur_time = double(cur_sample)/sample_rate
	else: # this is only needed in microphone mode. i'm not sure it will be needed when we integrate with the game...
	  time.sleep( . )

def is_finished():
	if(from_mic):
		return (not(snd.getPosition() <= time_to_record))
	else:
		return file_is_over

def stop_rec():
	if(from_mic):
		snd.stop()
	else:
		snd.close()
	   
def voiceRecorder(  ):
	global sound_events

	init()

	start_rec()

	# Loop until recorded position greater than the limit specified
	while (not(is_finished())):
		read_data()
		analyse_sound()
		for i in sound_events:
			( time , event_type , note_index , note_name ) = i
			print "%.f\t%d\t%d\t%s\t%f" % (time , event_type , note_index , note_name,float(note_index)*sample_rate/number_of_samples_to_process)
		sound_events = []
   
	# Stop listening the incoming sound from the microphone or line in
	stop_rec()

 
def analyse_sound():
	# if we processed just a short while ago, no need to run again. return.
	if (cur_time < last_processed_time + interval):
		return
	global last_processed_time
	last_processed_time = cur_time
	global sound_vector
	global sound_events
	sound_vector = sound_vector[-number_of_samples_to_process:]
	N=len(sound_vector)
	#print N
	S=abs(fft(sound_vector))
	#print len(S)
	f=sample_rate*r_[:(N/)]/N
	n=len(f)
	S = S[:n];
	S[:] = 

	# BEWARE - UGLY PATCH AHEAD
	# this line removes energy from the noisy Hz/Hz band
	#S[]=
	#S[]=
	#S[]=
	#S[]=

	if(peaks_only):
	   
		# BEWARE - UGLY PATCH AHEAD
		# the following lines remove overtones of detected notes.
		for j in now_playing.keys():
			S[floor(*j/.):ceil(*j*.)] = 
			S[floor(*j/.):ceil(*j*.)] = 
			S[floor(*j/.):ceil(*j*.)] = 
			S[floor(*j/.):ceil(*j*.)] = 

		# delete from the FFT all sounds that we already know that are playing,
		# and check if they stopped playing
		for j in now_playing.keys():
			# read parameters from last sample
			(time, last_power, max_power, last_area_power, max_area_power, was_decaying, detected_frames) = now_playing[j]
			v = double(j)*sample_rate/N
			# get current sample parameters
			curr_power = S[j]
			curr_area_power = sum(S[floor(j/.):ceil(j*.)])

			if(curr_power > MinPower):
				detected_frames += 

			if( detected_frames == DetectionFrames ):
				#sound_events.append((time, , j, find_closest_note(v)))
				#print "%d: %s (%d) started playing at volume %d"  % (cur_sample, find_closest_note(v),j,curr_area_power)
				detected_frames += 
							   
			# keep track of maximum power
			if(curr_power > max_power):
				max_power = curr_power

			# keep track of maximum power
			if(curr_area_power > max_area_power):
				max_area_power = curr_area_power

			# check if power is dropping
			if(curr_power < last_power * DecayFactor):
				was_decaying += 

			# if power is going up, and we have already seen it dropping - the sounds must have been played again.
			if((curr_power*ReplayFactor > last_power)and(was_decaying >= DecaySamplesNeeded)):
				was_decaying = 
				nn = find_closest_note(v)
				if(detected_frames >= DetectionFrames):
					sound_events.append((cur_time, , j, nn))
					sound_events.append((cur_time, , j, nn))
					print "%d: \t%s (%d) re-started playing" % (cur_sample, nn,j)
				#print "%.f: %s (%d) started playing" % (cur_time, nn,j)

			# update all parameters in our dict
			now_playing[j] = (time, curr_power, max_power, last_area_power, max_area_power, was_decaying, detected_frames )

			# remove power from the sonogram
			S[floor(j/.):ceil(j*.)] = 

			# check if note stopped = droped to . of maximum power
			#if ((curr_area_power < max_area_power * .)):
			#if (curr_area_power < StopAreaPower):
			if(curr_power < StopPower):
				now_playing.pop(j)
				#if(detected_frames >= DetectionFrames):
				sound_events.append((cur_time, , j, find_closest_note(v)))
				print "%.f: \t%s (%d) stopped playing at volume %d" % (cur_time, find_closest_note(j*sample_rate/N),j,curr_power)
			#if(j==):
			#    print "\t%.f %d %d %d %d %d " % (cur_time, curr_power, max_power, curr_area_power, max_area_power,was_decaying)
		   
		   
		# now look for new notes that are strong enough to be considered as playing
		flag=True
		while(flag):
			j = S.argmax(None)
			i = S[j]
			v = double(j)*sample_rate/N
			if((i>MinPower) and (v>) and (abs(v-)>)):
				t = sum(S[floor(j/.):ceil(j*.)])
				now_playing[j] = (cur_time, i,i, t, t, ,  )
				print "%d: %s (%d) started playing at volume %d"  % (cur_sample, find_closest_note(v),j,t)
				sound_events.append((cur_time, , j, find_closest_note(v)))
			   
				flag = False
			if(i<=MinPower):
				flag = False
			S[floor(j/.):ceil(j*.)] = 
		#j = S.argmax(None)
		#i = S[j]
		#v = double(j)*sample_rate/N
		#S[j-:j+] = 
		#print "%.f\t%.f\t%.f\t%s\t%.f\t%.f\t%s\t%.f" % (cur_time, double(cur_time)/sample_rate, v, find_closest_note(v),i,v, find_closest_note(v),i)
	   
	else: # not peaks_only - create full sonogram. mostly to export to matlab for research
		out = []
		St = ""
		for i in S:
			i = i/
			St+="%d," % i
		print St

# ----------------------------------------------------------------------------------

if __name__ == "__main__":
  if(len(sys.argv)==):
	  print "\n\n\nusage: "
	  print "to record from microphone:    %s <time to record in seconds>" % sys.argv[]
	  print "to read from file:            %s -f filename" % sys.argv[]
	  print "add \"-full\" to analyse full histogram\n\n\n"
	  sys.exit()
  try:
	  time_to_record = int(sys.argv[])
  except Exception,e:
	  pass
  for i in range(, len(sys.argv) ):
	  if sys.argv[i]=="-f":
		  filename = sys.argv[i+]
		  from_mic = False
	  if sys.argv[i]=="-full":
		  peaks_only = False
 
  voiceRecorder(  )
