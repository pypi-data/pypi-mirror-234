#
# from matplotlib.backend_bases import MouseButton
# import matplotlib.pyplot as plt
# import numpy as np
#
#
# %matplotlib
#
# t = np.arange(0.0, 1.0, 0.01)
# s = np.sin(2 * np.pi * t)
# # fig, ax = plt.subplots()
# # ax.plot(t, s)
#
#
# # def on_move(event):
#
# #     if event.inaxes:
#
# #         end = None
#
# #         start = event.xdata
#
# #         while event.button==MouseButton.LEFT:
# #             end = event.xdata
# #             # yield
#
# #         print(start,end)
#
#
# #     # if event.button==MouseButton.LEFT and event.button==MouseButton.LEFT:
# #     #     print(True)
# #         # if event.inaxes:
# #         #     print(f'data coords {event.xdata} {event.ydata},',
# #         #           f'pixel coords {event.x} {event.y}')
#
#
# def on_click(event):
#
#
#     if event.xdata!=None:
#
#         x,y = event.x, event.y
#
#         px, py = fig.transFigure.inverted().transform((x,y))
#
#         for i,ax in enumerate(event.inaxes.figure.axes):
#
#             bbox = ax.get_position()
#             legend = ax.get_legend()
#
#             if bbox.contains(px,py) and legend!=None:
#
#                 for line in ax.get_lines():
#
#                     legend_title = legend.get_title().get_text()
#                     label = line.get_label()
#
#                     print(legend_title,label)
#
#
#
#
#
# def on_release(event):
#     if event.button==MouseButton.LEFT:
#         print(event.xdata)
#
#
#
#
# # # binding_id = plt.connect('motion_notify_event', on_move)
# # plt.connect('button_press_event', on_click)
# # plt.connect('button_release_event', on_click)
#
# # plt.show()
#
#
# spot = np.random.random((10,10))
#
#
# import matplotlib.pyplot as plt
#
# # plt.close()
#
# # split = True
# # show_spot = True
# # n_figs = 1
# # num_lines = 4
#
# # fig = plt.figure(figsize=(8, 8))
#
# # outer_grid = fig.add_gridspec(n_figs, 1, hspace=0)
#
# # for i, outer_ax in enumerate(range(n_figs)):
#
# #     axes = fig.add_subplot(outer_grid[i, 0])
# #     axes.plot(t,s)
# #     axes.set_axis_off()
#
#
# #     if split==True:
#
# #         if num_lines > 1:
# #             if show_spot:
# #                 inner_grid = outer_grid[i, 0].subgridspec(ncols=2, nrows=num_lines, wspace=0, hspace=0)
# #                 sub_axes = inner_grid.subplots()
# #             else:
# #                 inner_grid = outer_grid[i, 0].subgridspec(ncols=1, nrows=num_lines, wspace=0, hspace=0)
# #                 sub_axes = np.expand_dims(inner_grid.subplots(),-1)
#
#
# #         else:
# #             sub_axes = [axes]
#
# #     else:
# #         sub_axes = [axes]*num_lines
#
#
#
# #     for j, ax in enumerate(sub_axes):
#
# #         ax[0].plot(t,s, label=f"line:{j}")
# #         ax[0].legend(loc="upper right", title = f"fig:{i}")
#
# #         if len(ax) > 1:
# #             ax[1].imshow(spot)
# #             ax[1].set_axis_off()
#
#
#
# # plt.connect('button_press_event', on_click)
#
#
#
# import matplotlib.pyplot as plt
# import matplotlib.gridspec as gridspec
# from matplotlib.patches import Rectangle
# import copy
#
#
# plt.close()
#
# split = True
# show_spot = True
# n_figs = 1
# num_lines = 3
#
#
# fig = plt.figure(figsize=(8, 8))
#
# outer_grid = gridspec.GridSpec(n_figs, 1, figure=fig)
#
# if n_figs==1:
#     outer_grid_axes = [outer_grid.subplots()]
# else:
#     outer_grid_axes = [ax for ax in outer_grid.subplots()]
#
# for i, axes in enumerate(outer_grid_axes):
#
#     if split==True and num_lines > 1:
#         if num_lines > 1:
#             axes.set_axis_off()
#             if show_spot:
#                 inner_grid = gridspec.GridSpecFromSubplotSpec(num_lines, 2, subplot_spec=outer_grid[i], width_ratios=[3,1], hspace=0, wspace=0.1)
#                 sub_axes = inner_grid.subplots()
#             else:
#                 inner_grid = gridspec.GridSpecFromSubplotSpec(num_lines, 1, subplot_spec=outer_grid[i], hspace=0, wspace=0)
#                 sub_axes = [[ax] for ax in inner_grid.subplots()]
#
#     else:
#         if show_spot:
#             inner_grid = gridspec.GridSpecFromSubplotSpec(1, 2, subplot_spec=outer_grid[i], width_ratios=[3,1], hspace=0, wspace=0.1)
#             inner_grid_axes = inner_grid.subplots()
#
#             spot_grid = inner_grid[1].subgridspec(num_lines,1, hspace=0.5)
#
#             if num_lines > 1:
#                 spot_grid_axes = [ax for ax in spot_grid.subplots()]
#             else:
#                 spot_grid_axes = [spot_grid.subplots()]
#
#             sub_axes = [[inner_grid_axes[0],spot_grid_axes[line]] for line in range(num_lines)]
#             axes.set_axis_off()
#             inner_grid_axes[1].set_axis_off()
#         else:
#             sub_axes = [[axes]]*num_lines
#
#
#
#     for j, ax in enumerate(sub_axes):
#
#         ax[0].plot(t,s, label=f"line:{j}")
#         ax[0].legend(loc="upper right", title = f"fig:{i}")
#
#         ymin, ymax = ax[0].get_ylim()
#         xcentre = 0.5
#         x_width = 0.1
#         rect = Rectangle((xcentre,ymin),x_width,(ymax-ymin),linewidth=1,edgecolor='r',facecolor='r')
#         ax[0].add_patch(rect)
#
#         if len(ax) > 1:
#
#             ax[1].imshow(spot,label="spot")
#             ax[1].set_axis_off()
#             ax[1].title.set_text("test")
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
