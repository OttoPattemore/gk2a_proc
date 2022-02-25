from PIL import Image
import sys
import os

# Jet color scheme adapted from https://stackoverflow.com/questions/7706339/grayscale-to-red-green-blue-matlab-jet-color-scale
def interpolate( val, y0, x0, y1, x1 ):
  return (val-x0)*(y1-y0)/(x1-x0) + y0

def blue( grayscale ):
  if ( grayscale < -0.33 ): return 1.0
  elif ( grayscale < 0.33 ): return interpolate( grayscale, 1.0, -0.33, 0.0, 0.33 );
  else: return 0.0

def green( grayscale ): 
  if ( grayscale < -1.0 ): return 0.0
  if  ( grayscale < -0.33 ): return interpolate( grayscale, 0.0, -1.0, 1.0, -0.33 );
  elif ( grayscale < 0.33 ): return 1.0
  elif ( grayscale <= 1.0 ): return interpolate( grayscale, 1.0, 0.33, 0.0, 1.0 );
  else: return 1.0

def red( grayscale ):
  if ( grayscale < -0.33 ):
    return 0.0
  elif ( grayscale < 0.33 ):
    return interpolate( grayscale, 0.0, -0.33, 1.0, 0.33 )
  else:
      return 1.0


def rain_fall(ir):
    apply  = Image.new("RGB", ir.size)
    apply.paste(ir)
    for x in range(0,ir.width):
        for y in range(0,ir.height):
            min_thermal = 200
            value = ir.getpixel((x,y))
            if type(value)==int:
                grey_scale  = value
            else:
                grey_scale = int((float(value[0])+float(value[1])+float(value[2]))/3.0)
            if(grey_scale > min_thermal):
                v  = (grey_scale-min_thermal)/(255-min_thermal)
                apply.putpixel((x,y),(int(red((v-0.5)*2)*255),int(green((v-0.5)*2)*255),int(blue((v-0.5)*2)*255)))

    return apply

def thermal(ir):
    apply  = Image.new("RGB", ir.size)
    for x in range(0,ir.width):
        for y in range(0,ir.height):
            value = ir.getpixel((x,y))/255
            r = int(red((value-0.5)*2)*255)
            g = int(green((value-0.5)*2)*255)
            b = int(blue((value-0.5)*2)*255)
            apply.putpixel((x,y),(r,g,b))
    return apply


def gk2a_proc(ir):
    return (thermal(ir),rain_fall(ir))
def main():
    if(len(sys.argv) < 3):
        print("Usage: ./gk2a_proc.py <input> <output directory>")
        exit(-1)
    input_image = sys.argv[1]
    output_directory = sys.argv[2]
    if not os.path.isdir(output_directory):
        os.mkdir(output_directory)
    
    therm, rain = gk2a_proc(Image.open(input_image))

    therm.save(output_directory+"/thermal.png")
    rain.save(output_directory+"/rainfall.png")
if __name__ == "__main__":
    main()