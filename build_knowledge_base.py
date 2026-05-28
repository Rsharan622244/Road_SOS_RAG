"""
Run this ONCE to build your knowledge base text files.
It creates the knowledge_base/ folder content automatically.
No PDFs needed — we write the content directly.
"""
import os

os.makedirs("knowledge_base", exist_ok=True)

# File 1: Road accident first aid
# with open("knowledge_base/first_aid.txt", "w") as f:
with open("knowledge_base/first_aid.txt", "w", encoding="utf-8") as f:
    f.write("""ROAD ACCIDENT FIRST AID GUIDE

GOLDEN HOUR
The golden hour refers to the first 60 minutes after a traumatic injury. Prompt medical care during this period significantly improves survival rates. Every second counts in a road accident emergency.

GENERAL STEPS AT ACCIDENT SCENE
1. Ensure your own safety first. Turn off your vehicle engine. Turn on hazard lights.
2. Call emergency services immediately: 112 (India), 911 (USA), 999 (UK).
3. Do not move injured persons unless there is immediate danger such as fire or flooding.
4. Keep the injured person warm, calm, and still.
5. Do not give food or water to an injured person.
6. Stay with the injured until help arrives.

UNCONSCIOUS PERSON
1. Check for breathing by looking for chest movement and listening near mouth.
2. If not breathing and you are trained, begin CPR: 30 chest compressions followed by 2 rescue breaths.
3. Place in recovery position if breathing: on their side with head tilted back to keep airway open.
4. Never move a person with suspected spinal or neck injury unless in immediate danger.
5. Keep checking breathing every minute until ambulance arrives.

HEAVY BLEEDING
1. Apply firm, direct pressure to the wound using a clean cloth or bandage.
2. Do not remove the cloth even if it becomes soaked — add more cloth on top.
3. Elevate the injured limb above the level of the heart if possible.
4. Do not apply a tourniquet unless bleeding is life-threatening and uncontrolled.
5. Keep pressure applied continuously until medical help arrives.

HEAD INJURY
1. Keep the person still and calm. Do not allow them to stand or walk.
2. Do not remove any object embedded in the head.
3. If unconscious but breathing, place in recovery position.
4. Watch for danger signs: unequal pupils, vomiting, seizures, worsening confusion.
5. Suspect spinal injury with every serious head injury — immobilize head and neck.

SPINAL INJURY
1. Do not move the person at all unless there is immediate danger.
2. Keep the head, neck, and spine aligned and still at all times.
3. If you must move them, keep the entire body in a straight line.
4. Reassure the person and keep them calm and warm.
5. Wait for trained paramedics — improper movement can cause permanent paralysis.

BROKEN BONES AND FRACTURES
1. Do not try to straighten a broken bone.
2. Immobilize the injured area using a makeshift splint if available.
3. Apply ice wrapped in cloth to reduce swelling — never directly on skin.
4. For open fractures where bone is visible, cover with a clean cloth but do not push bone back.
5. Keep the person still and calm until medical help arrives.

BURNS
1. Cool the burn immediately with cool running water for at least 10 minutes.
2. Do not use ice, butter, or toothpaste on burns.
3. Remove jewellery and clothing near the burn but not if stuck to skin.
4. Cover with a clean non-fluffy material such as cling film or a clean plastic bag.
5. For severe burns covering large areas, call 112 immediately and keep the person warm.

SHOCK
Signs of shock: pale or grey skin, cold and clammy skin, rapid shallow breathing, dizziness, confusion.
1. Lay the person down and raise their legs about 30cm if no leg injury is suspected.
2. Keep them warm with a blanket or jacket.
3. Do not give anything to eat or drink.
4. Loosen tight clothing around neck and chest.
5. Call 112 immediately — shock is life threatening.

CHILD INVOLVED IN ACCIDENT
1. Children are more vulnerable to internal injuries even without visible trauma.
2. Always take a child to hospital after any road accident regardless of apparent severity.
3. For infant CPR: use two fingers for chest compressions, gentler rescue breaths.
4. Keep child calm and with a familiar adult if possible.
5. Watch for delayed symptoms such as vomiting or unusual sleepiness.

MOTORCYCLE ACCIDENT
1. Do not remove a helmet from an injured motorcyclist unless airway is blocked.
2. Suspect spinal injury in all high-speed motorcycle crashes.
3. Road rash: flush with clean water, cover with clean bandage.
4. Check for internal injuries even if person appears fine externally.

VEHICLE FIRE
1. Get everyone out of the vehicle immediately.
2. Move at least 30 metres away from the vehicle.
3. Call 112 immediately.
4. Never go back into a burning vehicle.
5. Do not attempt to open the bonnet if smoke or flames are visible.
""")

# File 2: Emergency contacts and procedures
# with open("knowledge_base/emergency_procedures.txt", "w") as f:
with open("knowledge_base/emergency_procedures.txt", "w", encoding="utf-8") as f:
    f.write("""EMERGENCY CONTACTS AND PROCEDURES

INDIA EMERGENCY NUMBERS
- Police: 100
- Ambulance: 108
- Fire: 101
- National Emergency: 112 (works for all services)
- Highway Patrol: 1033
- Women Helpline: 1091
- Disaster Management: 1078

INTERNATIONAL EMERGENCY NUMBERS
- USA and Canada: 911
- United Kingdom: 999
- European Union: 112
- Australia: 000
- UAE: 999
- Singapore: 995
- Germany: 112
- France: 15 (ambulance), 17 (police), 18 (fire)
- Japan: 119 (ambulance and fire), 110 (police)

HOW TO CALL FOR EMERGENCY HELP
When you call emergency services, be ready to say:
1. Your exact location — landmark, road name, kilometre marker
2. What happened — type of accident, number of vehicles involved
3. How many people are injured and their condition
4. Whether anyone is unconscious, not breathing, or bleeding heavily
5. Your phone number in case the call drops
6. Stay on the line — do not hang up until told to do so

WHAT TO DO WHILE WAITING FOR AMBULANCE
1. Keep the injured person still and warm.
2. Monitor their breathing continuously.
3. Send someone to the road to wave down the ambulance.
4. Clear the area of unnecessary bystanders.
5. Note any changes in the person's condition to tell paramedics.
6. Do not move vehicles involved in the accident until police arrive.

REPORTING A ROAD ACCIDENT IN INDIA
1. Call 112 or 100 to report to police.
2. Note the time, location, vehicles involved and registration numbers.
3. Get names and contact details of witnesses.
4. Take photographs of the scene if safe to do so.
5. File an FIR (First Information Report) at the nearest police station.
6. Notify your insurance company within 24 hours.
7. Good Samaritan Law in India protects bystanders who help accident victims.

GOOD SAMARITAN LAW INDIA
Under the Good Samaritan Law in India:
- Any person who helps an accident victim in good faith is protected from legal liability.
- You cannot be detained, questioned, or made a witness if you take a victim to hospital.
- Hospitals must provide immediate treatment to accident victims without demanding payment first.
- You are protected from civil and criminal liability for actions taken in good faith to help.

TRAUMA CENTRE LEVELS
- Level 1 Trauma Centre: highest capability, 24/7 trauma surgeons, handles most critical cases
- Level 2 Trauma Centre: can handle most trauma cases, may transfer extremely critical patients
- Government hospitals in India: generally equipped for trauma care
- For critical accidents: ask specifically for the nearest Level 1 trauma centre or government hospital

TOWING AND VEHICLE RECOVERY
1. Do not move a vehicle involved in a serious accident until police give permission.
2. For breakdown without accident: you can call towing services immediately.
3. Keep the vehicle's hazard lights on and place warning triangles if available.
4. Note the vehicle's exact location for the towing service.
5. Get a written receipt from the towing service with destination address.
""")

# File 3: Road safety information  
# with open("knowledge_base/road_safety.txt", "w") as f:
with open("knowledge_base/road_safety.txt", "w", encoding="utf-8") as f:

    f.write("""ROAD SAFETY INFORMATION

COMMON CAUSES OF ROAD ACCIDENTS IN INDIA
1. Overspeeding: responsible for over 70% of fatal accidents
2. Drunk driving: impairs judgment and reaction time severely
3. Distracted driving: mobile phone use, eating while driving
4. Not wearing seatbelt: increases fatality risk by 3 times
5. Not wearing helmet: responsible for 45% of motorcycle deaths
6. Wrong side driving and dangerous overtaking
7. Running red lights and traffic signals
8. Poor road conditions: potholes, poor lighting, lack of signage
9. Fatigue driving: drowsy driving as dangerous as drunk driving
10. Not following lane discipline

HELMET SAFETY
- Always wear an ISI marked helmet that fits properly.
- Fasten the chin strap securely.
- Replace a helmet after any major impact even if no visible damage.
- A helmet reduces the risk of fatal head injury by 42%.
- Both rider and pillion must wear helmets — it is the law in India.

SEATBELT SAFETY
- Wear seatbelt on every journey, even short distances.
- Rear seat passengers must also wear seatbelts.
- A seatbelt reduces the risk of death in a crash by 50%.
- Pregnant women should still wear seatbelts — under the bump, not across the stomach.

SPEED AND SAFE DRIVING
- Urban areas in India: maximum 50 kmph
- National highways: maximum 100 kmph for cars
- Expressways: maximum 120 kmph for cars
- School zones and hospital zones: 25 kmph
- Always adjust speed for weather, road, and traffic conditions.

ALCOHOL AND DRIVING IN INDIA
- Legal blood alcohol limit: 30mg per 100ml of blood
- Penalty: up to 6 months imprisonment and Rs 10,000 fine for first offence
- There is no safe amount of alcohol for driving — any amount impairs reaction time.
- Plan ahead: designate a sober driver or use a cab service.

NIGHT DRIVING SAFETY
- Use headlights properly — full beam on empty roads, dip when oncoming traffic approaches.
- Reduce speed by at least 20% at night.
- Take breaks every 2 hours on long night drives.
- Watch for pedestrians, animals, and slow vehicles without lights.
- If feeling drowsy, pull over safely and rest — do not continue driving.

HIGHWAY SAFETY
- Maintain safe following distance: at least 3 seconds gap from vehicle ahead.
- Check mirrors every 5-8 seconds.
- Avoid stopping on highway shoulders unless emergency.
- Use hazard lights if your speed drops suddenly.
- Keep emergency kit: first aid box, warning triangle, torch, tow rope.
""")

print("Knowledge base created successfully!")
print("Files created:")
for f in os.listdir("knowledge_base"):
    size = os.path.getsize(f"knowledge_base/{f}")
    print(f"  knowledge_base/{f} ({size} bytes)")