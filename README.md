# Cenda Tools
Addons for Blender (Mainly for animators)

Read full description here:
https://blenderartists.org/forum/showthread.php?405910-Addon-Cenda-Tools

Hello, I created this thread to publish my addons that I've made during production. I am using it both for my personal projects, and mostly when creating animations for our latest game Planet Nomads. You can check it here: https://www.planet-nomads.com/

As an ex-Autodesk user (3dsmax, Maya, Softimge ) I didn`t like some of the behaviour or miss some little things in Blender. So I created these addons. I also hope that this thread will be read by some Blender developers so I am also adding suggestions on how it can be implemented into Blender 

I am not using any auto-assign hotkeys, because I use my custom hotkeys in Blender, and I don`t know what works best for you. You can easily add it to your hotkey settings as you please.

I am also new at scripting in Blender, so I believe that many of you can do the same thing better, so please take these as prototypes. Any Pull requests to my GitHub are welcome!


EXPORT FBX

During game development you are doing so many changes and it is very tedious to constantly click FILE > EXPORT > FBX > set preset > find your file, etc. So here is a simple one-button solution.

Just fill the export paths (it is saved with scene), select objects for export and click the Export button. Backup is doing a copy of the exported FBX. It is prepared for exporting to Unity and fit to my workflow. Just change the code for different settings.

Location: Tools > Export to FBX 
Download: https://github.com/CenekStrichel/CendaTools/blob/master/cs_export_fbx.py


BAKE & UNBAKE

If you bake your rigid body, you lose all your previous settings .. sad. But not with Unbake  With this addon you can load your previous settings and bake again right away.

It saves all your settings to the object and later loads them back. You can even Save and Load your settings without baking.



Location: Physics > Rigid Body Settings
Download: https://github.com/CenekStrichel/CendaTools/blob/master/cs_bake_unbake.py

For Blender developers:
If you add settings to enable / disable physics for rigid body instead of simply removing it, the problem with lost settings will be solved.




OFFSET ANIMATION

Offseting for animated bones like in 3dsmax when you turn off Set key. But it is working only for one bone now. I think the GIF below is self explainig.


Location: Tools > Offset Animation (Pose Mode)
Download: https://github.com/CenekStrichel/CendaTools/blob/master/cs_offset_animation.py

For Blender developers:
It would be great if Blender had a function for Offseting animation. For example add Offset Mode on the Timeline and any change you do in View3D will be reflected as offset for the f-curve.


RIG SWITCHER

I really love Modes in Blender (Pose, Edit, Weight) But if you want to make any changes, you still have to modify too many things. You need different bone layers for Pose, different layers for Weight, etc. Sometimes it is also better to change the draw display. Rig switcher is doing this in one step. It also hides lower LODs or makes meshes unselectable during Posing.

Setup:

“Setup Bones by Prefix” button is moving bones to the right layer by their Deform settings, DEF- prefix or MCH- prefix.

Rig switcher Pie Menu:

Add “wm.call_menu_pie” to Input Preferences with the parameter: “VIEW3D_MT_rig_switcher_menu” in 3D View section.

Rig switcher in action:



Location: Setup is in the Armature setting, Pie menu command must be added to the Input Preferences
Download: https://github.com/CenekStrichel/CendaTools/blob/master/cs_rig_switcher.py


IK SETUP

It is the same as the traditional IK setup, but it will do a few things automatically for you:
Set chain length by hiearchy (you can change it manualy)
Create custom IK parameter for FK/IK Blending



Location: Pose > Inverse Kinematics > Add IK to Bone with Auto Chain
Download: https://github.com/CenekStrichel/CendaTools/blob/master/cs_ik_setup.py


KEYING TOOLS

This will a bit hard to explain, but let's get to it  Firstly, some explanation. Because I used many types of 3D software before Blender, I really don't like the keying behaviour in Blender. It is creating too many redundant keys. Autokey has the same problem as well. Although there is the “Only Insert Needed” setting in Options, you cannot use it to add static keys. So I am keying everything with my script. It turns off the “Only Insert Needed”, it keys only the unlocked channels and turns “Only Insert Needed” back to its previous state. With this behaviour I can use Autokey for only keying the modified channels and also add my own static keys.

I recommend turning on AutoKey and Only Insert Needed if you want to use this script.
Location: Timeline header



There is also a menu for keying separate channels with the same keying logic:
Just add a hotkey command: “wm.call_menu” with “ANIM_MT_insert_keyframes_menu” parameter in Input Preferences.



For Blender developers:
If you add the option “Only Insert Needed (Autokey only)” as enum for example, the problem will be solved.

In View3D you can also find these buttons:

Auto IK - standard auto ik, only in headbar because it is faster  I am using a hotkey for this function, but it is great as a state indicator too.

Button next to this one is “Copy and Paste Flipped”. Yes it is super simple and my first script ever  But I very often need to copy and paste flipped. So it is done in one step.

In the Dopesheet there are tools for locomotion animation. Rember to check “Only selected” and animate just one side of the character. Then select the animated bones and click on “Offseted” to get offsetted locomotion (offset is taken from frame range) OR “No Offset” to have a mirrored locomotion.
Mirror Action will just copy and paste flipped animation keys. So when your character is walking forward left, it will change to forward right. The script does a very simple thing, but it is used so often, it saves quite some time.



Locomotion in action:


Location: Timeline header, View3D header, Dopesheet (only selected mode) header
Download: https://github.com/CenekStrichel/CendaTools/blob/master/cs_keying_tools.py

So that is all for today, the next bunch of addons will be added soon (below). They are all on Github already, but without any explanation, they might be hard to use. So wait until I release the explanation to those and don't ask about them just yet  Feel free to ask about the above addons.


CHANGE FRAME (WITH DRAG)

Change the current frame by dragging it in viewport



Settings in Input Preferences



Add “view3d.change_frame_drag” under 3D View (Global) and set it as you wish.

Auto Sensitivity - sensitivity is taken from timerange length
Sensitivity - if Auto Sensitivity is False, this value is used
End Drag - You have to use the same mouse button used to start dragging

Location: View3D + drag mouse
Download: https://github.com/CenekStrichel/CendaTools/blob/master/cs_change_frame.py


QUICK MOTION PATHS

It is practically the same as ordinary Motion Paths Calculate, but without the floating dialog for Start and End settings. These parameters are set from timerange. 



Location: Tools > Quick Motion Paths
Download: https://github.com/CenekStrichel/CendaTools/blob/master/cs_quick_motion_path.py


BONES RENAMER

I very often need to duplicate extremities for animals. This is a simple rename tool for newly created bones.



Location: Tools > Bones Renamer (Armature Edit Mode)
Download: https://github.com/CenekStrichel/CendaTools/blob/master/cs_bones_rename.py


Remaining addons
Animation Constraint - For baking constraint with props
Editor Switcher - Pie menu with editor switch
Get Step Length - Synchronize length step for quadruped
Numeric Selector - Select character bones with Numpad keys
Render Region - not working .. don`t use it else 
Tools - Many little tools without category
