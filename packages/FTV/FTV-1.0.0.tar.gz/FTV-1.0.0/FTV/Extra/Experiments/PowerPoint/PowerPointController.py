import win32com.client

pptApp = win32com.client.GetActiveObject("PowerPoint.Application")
pptPres = pptApp.Presentations(1)

# for slide in pptPres.Slides:
#     print(f"{slide.Name}: {slide.SlideNumber}")

pptPres.Slides(1).Select()
pptPres.SlideShowSettings.Run()
pptView = pptApp.SlideShowWindows(1).View

# pptView.GotoSlide(1)

min_slide_pos = 1
max_slide_pos = len(pptPres.Slides)

isStop = False
while not isStop:
    slide_pos_str = input(f"Please select a slide number (1 to {max_slide_pos}): ")

    if slide_pos_str.lower() == "p":
        isStop = True

    else:
        try:
            slide_pos = int(slide_pos_str)
            if min_slide_pos <= slide_pos <= max_slide_pos:
                pptView.GotoSlide(slide_pos)
            else:
                raise IndexError()

        except ValueError as e:
            print(f"Please type only slide numbers or 'p' to pause the presentation.")
            # print(e.with_traceback())
        except IndexError as e:
            print(f"Please type only numbers in the range {min_slide_pos} to {max_slide_pos}.")
            # print(e.message)

pptApp.SlideShowWindows(1).View.Exit()
print()
print(f"The presentation, \"{pptPres.Name}\", has been stopped.")
