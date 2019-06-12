import facebook
access_token = "EAAfiVkmtayABABzItZAONAH5TKJD0mWcOHy9wxERdG9bLI8WRCxgAHCJvlmemlnaJZC785tHhTMQ3RwQjTlQMRIq8aX2qXFjp3nH9EkHlbBNgXvcMsXqNlcMIiYHAAhnse7wrAoqeCxRLcXaxUst9T9eF7Vg8XZC7AaOZCKBknP4QpIaJnmdfy19sJzIgOOzDkbC3J0sSwZDZD"
fb = facebook.GraphAPI(access_token)

fields = ['email, gender','name']

#profile = fb.get_                           object('me', fields=fields)

#print(profile)
#
# from scipy.stats import linregress
# from scipy import mean
# import numpy as np
#
# xs = [1,2,3,4,5,6,7,8,9,10,11,12]
# ys = [31,71,54,73,52,48,54,87,58,63,91,86]
#
# # # x2 = 6.0
# # # y2 = 5.0
# # slope, intercept, r_value, p_value, std_err = linregress([x1],[y1])
# # print(slope,intercept)
#
# xs = np.array([1,2,3,4,5,6],dtype=np.float64)
# ys= np.array([5,4,6,5,6,7],dtype=np.float64)
#
# def best_fit(xs,ys):
#     m = (((mean(xs)*mean(ys)) - mean(xs*ys)) /
#         ((mean(xs)*mean(xs)) - mean(xs*xs)))
#
#     b = mean(ys) - m * mean(xs)
#     return m, b
#
# m,b = best_fit(xs,ys)
# print(m, b)
#
# regression_line = [(m*x)+b for x in xs]
# print(regression_line)