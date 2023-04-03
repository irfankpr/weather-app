import streamlit as st
import requests as rq
import geocoder as geo
headers={
   "authorization":st.secrets["OW_key"]
}
st.markdown("""
<style>
   .egzxvld1, .e1pxm3bq0 {
       display: none;
    }
    #MainMenu {
       display: none;
    }
    
</style>
""",unsafe_allow_html=True)

OW_key=headers["authorization"]
def find_by_name(place):
   url = f"https://api.openweathermap.org/data/2.5/weather?q={place}&appid={OW_key}"
   weather = rq.post(url).json()
   try:
      coord=weather["coord"]
      more=weather["weather"][0]
      main=weather["main"]
      zone=weather["name"]
      st.session_state["weather_state"]=True
      return coord,more,main,zone
   except KeyError:
      st.error("No place found, please verify the name !")
      st.stop()
   
   

def find_by_loc():
   myloc=geo.ip("me")
   try:   
      weather=rq.post(f"https://api.openweathermap.org/data/2.5/weather?lat={myloc.latlng[0]}&lon={myloc.latlng[1]}&appid={OW_key}").json()
      coord=weather["coord"]
      more=weather["weather"][0]
      main=weather["main"]
      zone=weather["name"]
      st.session_state["weather_state"]=True
      return coord,more,main,zone

   except KeyError:
      st.error("No place found, please verify the name !")
      st.stop()
      
   

def main():
   st.markdown("<h1 style='text-align: center; color: CadetBlue;'>Weather App</h1>", unsafe_allow_html=True)
   place = st.text_input("Enter the Place").lower().strip()
   c1,c2,c3=st.columns([.5,3,1])
   show= c1.button("Show")
   loc = c3.button("my location")
   if show:
      if place == "":
         c2.error(" Please enter the place or use my location.")
         st.stop()
      coord,more,main,zone=find_by_name(place)

   if loc:
      coord,more,main,zone=find_by_loc()

   if st.session_state["weather_state"]:
      try:
         c1,c2=st.columns(2)
         unit =" °C"
         t=str(round(main["temp"]-273.15,4))+unit
         avg=round((main["temp_min"]+main["temp_max"])/2-273.15,4)

         c1.metric(label=zone,value=t)
         c1.write(f"latlong - {coord['lon']} : {coord['lat']}")
         c1.header(f"feels like {round(main['feels_like']-273.15,4)}")

         c2.image(f"https://openweathermap.org/img/wn/{ more['icon'] }@2x.png")
         c2.write(more["description"])
         c2.write(f"humidity: {main['humidity']}")
      except KeyError:
         st.error("No place found, please verify the name !")
      except:
         st.warning("something went wrong please try again")
         st.stop()
   else:
      st.stop()


if __name__ == "__main__":
   st.session_state["weather_state"]=False
   main()