import requests
import xml.etree.ElementTree as ET
import re

def main():
    url = "https://github-readme-activity-graph.vercel.app/graph?username=Shardz4&bg_color=1D2B53&color=F8F8F8&title_color=FBD000&line=5C94FC&point=E52521&area=true&area_color=5C94FC&border_color=1A1A1A&hide_border=false"
    print(f"Fetching contribution graph from: {url}")
    
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to fetch graph")
        return
        
    # Register namespaces to prevent namespace prefixes like ns0:
    ET.register_namespace("", "http://www.w3.org/2000/svg")
    
    # Parse the SVG XML
    root = ET.fromstring(response.content)
    
    # Find the line path (does not start with M90,350 which is the filled area path)
    line_path_d = None
    for path in root.findall('.//{http://www.w3.org/2000/svg}path'):
        d = path.attrib.get('d', '')
        if d and not d.startswith('M90,350'):
            line_path_d = d
            break
            
    if not line_path_d:
        print("Could not find the line path in the SVG")
        return
        
    print(f"Found line path: {line_path_d[:100]}...")
    
    # Mario pixel rects generated from our NES model
    # Width=40, Height=40. Origin at top-left.
    # To place Mario's feet (y=40) exactly on the line, we translate the inner group by (-20, -40).
    mario_rects = """
        <rect x="32.5" y="0.0" width="7.5" height="2.5" fill="#FCD7B6"/>
        <rect x="15.0" y="2.5" width="12.5" height="2.5" fill="#E52521"/>
        <rect x="32.5" y="2.5" width="7.5" height="2.5" fill="#FCD7B6"/>
        <rect x="12.5" y="5.0" width="22.5" height="2.5" fill="#E52521"/>
        <rect x="35.0" y="5.0" width="5.0" height="2.5" fill="#FCD7B6"/>
        <rect x="12.5" y="7.5" width="7.5" height="2.5" fill="#B85B14"/>
        <rect x="20.0" y="7.5" width="5.0" height="2.5" fill="#FCD7B6"/>
        <rect x="25.0" y="7.5" width="2.5" height="2.5" fill="#B85B14"/>
        <rect x="27.5" y="7.5" width="2.5" height="2.5" fill="#FCD7B6"/>
        <rect x="32.5" y="7.5" width="7.5" height="2.5" fill="#B85B14"/>
        <rect x="10.0" y="10.0" width="2.5" height="2.5" fill="#B85B14"/>
        <rect x="12.5" y="10.0" width="2.5" height="2.5" fill="#FCD7B6"/>
        <rect x="15.0" y="10.0" width="2.5" height="2.5" fill="#B85B14"/>
        <rect x="17.5" y="10.0" width="7.5" height="2.5" fill="#FCD7B6"/>
        <rect x="25.0" y="10.0" width="2.5" height="2.5" fill="#B85B14"/>
        <rect x="27.5" y="10.0" width="5.0" height="2.5" fill="#FCD7B6"/>
        <rect x="32.5" y="10.0" width="7.5" height="2.5" fill="#B85B14"/>
        <rect x="10.0" y="12.5" width="2.5" height="2.5" fill="#B85B14"/>
        <rect x="12.5" y="12.5" width="2.5" height="2.5" fill="#FCD7B6"/>
        <rect x="15.0" y="12.5" width="5.0" height="2.5" fill="#B85B14"/>
        <rect x="20.0" y="12.5" width="7.5" height="2.5" fill="#FCD7B6"/>
        <rect x="27.5" y="12.5" width="2.5" height="2.5" fill="#B85B14"/>
        <rect x="30.0" y="12.5" width="7.5" height="2.5" fill="#FCD7B6"/>
        <rect x="37.5" y="12.5" width="2.5" height="2.5" fill="#B85B14"/>
        <rect x="10.0" y="15.0" width="5.0" height="2.5" fill="#B85B14"/>
        <rect x="15.0" y="15.0" width="10.0" height="2.5" fill="#FCD7B6"/>
        <rect x="25.0" y="15.0" width="12.5" height="2.5" fill="#B85B14"/>
        <rect x="15.0" y="17.5" width="17.5" height="2.5" fill="#FCD7B6"/>
        <rect x="32.5" y="17.5" width="2.5" height="2.5" fill="#B85B14"/>
        <rect x="5.0" y="20.0" width="12.5" height="2.5" fill="#B85B14"/>
        <rect x="17.5" y="20.0" width="2.5" height="2.5" fill="#E52521"/>
        <rect x="20.0" y="20.0" width="7.5" height="2.5" fill="#B85B14"/>
        <rect x="27.5" y="20.0" width="2.5" height="2.5" fill="#E52521"/>
        <rect x="30.0" y="20.0" width="2.5" height="2.5" fill="#B85B14"/>
        <rect x="2.5" y="22.5" width="17.5" height="2.5" fill="#B85B14"/>
        <rect x="20.0" y="22.5" width="2.5" height="2.5" fill="#E52521"/>
        <rect x="22.5" y="22.5" width="7.5" height="2.5" fill="#B85B14"/>
        <rect x="30.0" y="22.5" width="2.5" height="2.5" fill="#E52521"/>
        <rect x="37.5" y="22.5" width="2.5" height="2.5" fill="#B85B14"/>
        <rect x="0.0" y="25.0" width="5.0" height="2.5" fill="#FCD7B6"/>
        <rect x="5.0" y="25.0" width="15.0" height="2.5" fill="#B85B14"/>
        <rect x="20.0" y="25.0" width="12.5" height="2.5" fill="#E52521"/>
        <rect x="37.5" y="25.0" width="2.5" height="2.5" fill="#B85B14"/>
        <rect x="0.0" y="27.5" width="7.5" height="2.5" fill="#FCD7B6"/>
        <rect x="10.0" y="27.5" width="5.0" height="2.5" fill="#E52521"/>
        <rect x="15.0" y="27.5" width="2.5" height="2.5" fill="#B85B14"/>
        <rect x="17.5" y="27.5" width="5.0" height="2.5" fill="#E52521"/>
        <rect x="22.5" y="27.5" width="2.5" height="2.5" fill="#FCD7B6"/>
        <rect x="25.0" y="27.5" width="5.0" height="2.5" fill="#E52521"/>
        <rect x="30.0" y="27.5" width="2.5" height="2.5" fill="#FCD7B6"/>
        <rect x="32.5" y="27.5" width="2.5" height="2.5" fill="#E52521"/>
        <rect x="35.0" y="27.5" width="5.0" height="2.5" fill="#B85B14"/>
        <rect x="2.5" y="30.0" width="2.5" height="2.5" fill="#FCD7B6"/>
        <rect x="7.5" y="30.0" width="2.5" height="2.5" fill="#B85B14"/>
        <rect x="10.0" y="30.0" width="25.0" height="2.5" fill="#E52521"/>
        <rect x="35.0" y="30.0" width="5.0" height="2.5" fill="#B85B14"/>
        <rect x="5.0" y="32.5" width="7.5" height="2.5" fill="#B85B14"/>
        <rect x="12.5" y="32.5" width="22.5" height="2.5" fill="#E52521"/>
        <rect x="35.0" y="32.5" width="5.0" height="2.5" fill="#B85B14"/>
        <rect x="2.5" y="35.0" width="7.5" height="2.5" fill="#B85B14"/>
        <rect x="10.0" y="35.0" width="17.5" height="2.5" fill="#E52521"/>
        <rect x="2.5" y="37.5" width="2.5" height="2.5" fill="#B85B14"/>
        <rect x="10.0" y="37.5" width="10.0" height="2.5" fill="#E52521"/>
    """
    
    # Create the animated group node
    animated_group_str = f"""
    <g xmlns="http://www.w3.org/2000/svg">
        <g>
            <!-- Motion animation following the line path -->
            <animateMotion 
                path="{line_path_d}" 
                dur="14s" 
                repeatCount="indefinite" 
                rotate="auto"
                calcMode="linear"
            />
            <!-- Inner group to perform local vertical jump animations relative to the moving path -->
            <g>
                <animateTransform
                    attributeName="transform"
                    type="translate"
                    values="-20,-40; -20,-75; -20,-40"
                    keyTimes="0; 0.5; 1"
                    dur="0.7s"
                    repeatCount="indefinite"
                />
                {mario_rects}
            </g>
        </g>
    </g>
    """
    
    # Parse the group string and append to the root of SVG
    animated_group = ET.fromstring(animated_group_str)
    root.append(animated_group)
    
    # Write the updated SVG to assets/animated-activity.svg
    output_path = "assets/animated-activity.svg"
    ET.ElementTree(root).write(output_path, encoding="utf-8", xml_declaration=True)
    print(f"Successfully generated animated graph SVG at: {output_path}")

if __name__ == "__main__":
    main()
