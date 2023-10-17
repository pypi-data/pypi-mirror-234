import os
import streamlit.components.v1 as components

_RELEASE = True

if not _RELEASE:
    _custom_bar_chart = components.declare_component(
        "custom_bar_chart",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _custom_bar_chart = components.declare_component("custom_bar_chart", path=build_dir)

def custom_bar_chart(
        chartData=None, 
        imgData=None, 
        mainContainerStyles=None, 
        barText=None,
        normalChart=None, 
        style=None, 
        chartLayout=None, 
        totalsConfig=None, 
        customChartTextLayout=None,
        # yValTotals=None, 
        key=None):
   
    component_value = _custom_bar_chart(
        chartData=chartData, 
        imgData=imgData, 
        mainContainerStyles=mainContainerStyles, 
        barText=barText, 
        normalChart=normalChart, 
        style=style, 
        chartLayout=chartLayout,
        totalsConfig=totalsConfig, 
        customChartTextLayout=customChartTextLayout,
        # yValTotals=yValTotals,
        key=key, 
        default=0)

    return component_value

if not _RELEASE:
    import streamlit as st
    st.set_page_config(layout="wide")

    style = {
        'bar-chart-container':{},
        'bar-chart-element':{},
        'bar-chart':{},
        'legend-container':{},
        'legend-items':{},
        'legend-img':{},
        'legend-label':{}
    }

    chartLayout = {
        "innerPadding":4,
        "padding":0.3,
        "layout":"vertical",
        "labelSkipWidth":25,
        "labelSkipHeight":20,
        "keys":[
            "demon-hunter-sword",
            "corrosion-scythe",
            "golden-staff",
            "wind-of-nature",
            "war-axe",
            "donut"
        ],
        "indexBy":"country",
        "isInteractive":True,
        "enableGridY":False,
        "axisLeft": None,
        "margin":{
            "top": 120,
            "right": 190,
            "bottom": 100,
            "left": 190
        },
        "enableLabel":True,
        "axisBottom": {
            "tickPadding":19
        }
    }

    chartLayoutsx = {
        "innerPadding":4,
        "padding":0.3,
        "layout":"horizontal",
        "labelSkipWidth":25,
        "labelSkipHeight":20,
        "keys":[
            "demon-hunter-sword",
            "corrosion-scythe",
            "golden-staff",
            "wind-of-nature",
            "war-axe",
            "donut"
        ],
        "indexBy":"country",
        "isInteractive":True,
        "enableGridY":True,
        "axisLeft": {
            "tickSize": 5,
            "tickPadding": 5,
            "tickRotation": 0,
            "legend": "Effect",
            "legendPosition": "middle",
            "legendOffset": -40
          },
        "margin":{
            "top": 120,
            "right": 190,
            "bottom": 100,
            "left": 190
        },
        "enableLabel":True,
        "axisBottom": {
            "tickPadding":19
        }
    }

    chartData = [
    {
      "country": "A-D",
      "demon-hunter-sword": 83,
      "demon-hunter-swordColor": "hsl(272, 70%, 50%)",
      "corrosion-scythe": 87,
      "corrosion-scytheColor": "hsl(329, 70%, 50%)",
      "golden-staff": 180,
      "goldern-staffColor": "hsl(37, 70%, 50%)",
      "wind-of-nature": 138,
      "wind-of-natureColor": "hsl(160, 70%, 50%)",
      "war-axe": 70,
      "war-exeColor": "hsl(328, 70%, 50%)",
      "donut": 198,
      "donutColor": "hsl(208, 70%, 50%)",
    },
    {
        "country": "AD",
        "demon-hunter-sword": 83,
        "demon-hunter-swordColor": "hsl(272, 70%, 50%)",
        "corrosion-scythe": 87,
        "corrosion-scytheColor": "hsl(329, 70%, 50%)",
        "golden-staff": 180,
        "goldern-staffColor": "hsl(37, 70%, 50%)",
        "wind-of-nature": 138,
        "wind-of-natureColor": "hsl(160, 70%, 50%)",
        "war-axe": 70,
        "war-exeColor": "hsl(328, 70%, 50%)",
        "donut": 198,
        "donutColor": "hsl(208, 70%, 50%)",
      },
    {
      "country": "AE",
      "demon-hunter-sword": 185,
      "demon-hunter-swordColor": "hsl(320, 70%, 50%)",
      "corrosion-scythe": 126,
      "corrosion-scytheColor": "hsl(81, 70%, 50%)",
      "golden-staff": 1,
      "goldern-staffColor": "hsl(100, 70%, 50%)",
      "wind-of-nature": 22,
      "wind-of-natureColor": "hsl(19, 70%, 50%)",
      "war-axe": 176,
      "war-exeColor": "hsl(72, 70%, 50%)",
      "donut": 177,
      "donutColor": "hsl(141, 70%, 50%)"
    },
    {
      "country": "AF",
      "demon-hunter-sword": 65,
      "demon-hunter-swordColor": "hsl(316, 70%, 50%)",
      "corrosion-scythe": 12,
      "corrosion-scytheColor": "hsl(223, 70%, 50%)",
      "golden-staff": 87,
      "goldern-staffColor": "hsl(0, 70%, 50%)",
      "wind-of-nature": 119,
      "wind-of-natureColor": "hsl(96, 70%, 50%)",
      "war-axe": 80,
      "war-exeColor": "hsl(167, 70%, 50%)",
      "donut": 145,
      "donutColor": "hsl(177, 70%, 50%)"
    },
    {
      "country": "Attack Speed",
      "demon-hunter-sword": 181,
      "demon-hunter-swordColor": "hsl(340, 70%, 50%)",
      "corrosion-scythe": 48,
      "corrosion-scytheColor": "hsl(223, 70%, 50%)",
      "golden-staff": 22,
      "goldern-staffColor": "hsl(319, 70%, 50%)",
      "wind-of-nature": 95,
      "wind-of-natureColor": "hsl(169, 70%, 50%)",
      "war-axe": 123,
      "war-exeColor": "hsl(279, 70%, 50%)",
      "donut": 15,
      "donutColor": "hsl(36, 70%, 50%)"
    },
    {
      "country": "Physical Attack",
      "demon-hunter-sword": 1,
      "demon-hunter-swordColor": "hsl(135, 70%, 50%)",
      "corrosion-scythe": 152,
      "corrosion-scytheColor": "hsl(17, 70%, 50%)",
      "golden-staff": 83,
      "goldern-staffColor": "hsl(281, 70%, 50%)",
      "wind-of-nature": 39,
      "wind-of-natureColor": "hsl(221, 70%, 50%)",
      "war-axe": 114,
      "war-exeColor": "hsl(13, 70%, 50%)",
      "donut": 143,
      "donutColor": "hsl(250, 70%, 50%)"
    },
    {
      "country": "Magic Power",
      "demon-hunter-sword": 45,
      "demon-hunter-swordColor": "hsl(66, 70%, 50%)",
      "corrosion-scythe": 20,
      "corrosion-scytheColor": "hsl(13, 70%, 50%)",
      "golden-staff": 10,
      "goldern-staffColor": "hsl(131, 70%, 50%)",
      "wind-of-nature": 140,
      "wind-of-natureColor": "hsl(175, 70%, 50%)",
      "war-axe": 143,
      "war-exeColor": "hsl(24, 70%, 50%)",
      "donut": 151,
      "donutColor": "hsl(306, 70%, 50%)"
    },
    {
      "country": "Defense",
      "demon-hunter-sword": 76,
      "demon-hunter-swordColor": "hsl(117, 70%, 50%)",
      "corrosion-scythe": 48,
      "corrosion-scytheColor": "hsl(334, 70%, 50%)",
      "golden-staff": 100,
      "goldern-staffColor": "hsl(5, 70%, 50%)",
      "wind-of-nature": 118,
      "wind-of-natureColor": "hsl(328, 70%, 50%)",
      "war-axe": 17,
      "war-exeColor": "hsl(115, 70%, 50%)",
      "donut": 162,
      "donutColor": "hsl(164, 70%, 50%)"
    },
    {
        "country": "Lifesteal",
        "demon-hunter-sword": 76,
        "demon-hunter-swordColor": "hsl(117, 70%, 50%)",
        "corrosion-scythe": 48,
        "corrosion-scytheColor": "hsl(334, 70%, 50%)",
        "golden-staff": 9,
        "goldern-staffColor": "hsl(5, 70%, 50%)",
        "wind-of-nature": 118,
        "wind-of-natureColor": "hsl(328, 70%, 50%)",
        "war-axe": 17,
        "war-exeColor": "hsl(115, 70%, 50%)",
        "donut": 162,
        "donutColor": "hsl(164, 70%, 50%)"
      },
      {
        "country": "Magic Lifesteal",
        "demon-hunter-sword": 76,
        "demon-hunter-swordColor": "hsl(117, 70%, 50%)",
        "corrosion-scythe": 48,
        "corrosion-scytheColor": "hsl(334, 70%, 50%)",
        "golden-staff": 67,
        "goldern-staffColor": "hsl(5, 70%, 50%)",
        "wind-of-nature": 118,
        "wind-of-natureColor": "hsl(328, 70%, 50%)",
        "war-axe": 17,
        "war-exeColor": "hsl(115, 70%, 50%)",
        "donut": 162,
        "donutColor": "hsl(164, 70%, 50%)"
      }
  ]
    
    imgData=[
    {
      "id": "demon-hunter-sword",
      "equipment":
        "https://static.expertwm.com/mlbb/items/demon-hunter-sword.png?w=64"
    },
    {
      "id": "corrosion-scythe",
      "equipment":
        "https://static.expertwm.com/mlbb/items/corrosion-scythe.png?w=64"
    },
    {
      "id": "golden-staff",
      "equipment": "https://static.expertwm.com/mlbb/items/golden-staff.png?w=64"
    },
    {
      "id": "wind-of-nature",
      "equipment": "https://static.expertwm.com/mlbb/items/wind-of-nature.png?w=64"
    },
    {
      "id": "war-axe",
      "equipment": "https://static.expertwm.com/mlbb/items/war-axe.png?w=64"
    }
  ]
    
    customChartTextLayout={
        "fontWeight":900,
        "fontSize":"17px",
        "fill":"white"
    }
    
    barText = {"x":None, "y":None}

    normalChart = False 

    mainContainerStyles={"elevation":0}

    totalsConfig={'showTotals':True, 'yValTotals':90, } #'textTotals':None,

   
    custom_bar_chart(chartData=chartData, imgData=imgData, mainContainerStyles=mainContainerStyles, barText=barText, normalChart=normalChart, style=style, chartLayout=chartLayout, totalsConfig=totalsConfig, customChartTextLayout=customChartTextLayout)

   