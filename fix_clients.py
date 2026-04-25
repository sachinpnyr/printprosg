#!/usr/bin/env python3
"""Fix clients section to use SVG logos instead of nearly-transparent PNG files"""

with open('index.html', 'r') as f:
    content = f.read()

# Find the clients-track div
start = content.find('<div class="clients-track">')
end = content.find('</div>', start) + 6

old_section = content[start:end]

new_section = '''<div class="clients-track">
        <img src="img/clients/marina-bay-hotels.svg" alt="Marina Bay Hotels" loading="lazy" />
        <img src="img/clients/greentech-asia.svg" alt="GreenTech Asia" loading="lazy" />
        <img src="img/clients/nexus-media.svg" alt="Nexus Media" loading="lazy" />
        <img src="img/clients/orbit-tech.svg" alt="Orbit Tech" loading="lazy" />
        <img src="img/clients/pearl-events.svg" alt="Pearl Events" loading="lazy" />
        <img src="img/clients/skyline-properties.svg" alt="Skyline Properties" loading="lazy" />
        <img src="img/clients/titan-logistics.svg" alt="Titan Logistics" loading="lazy" />
        <img src="img/clients/vantage-capital.svg" alt="Vantage Capital" loading="lazy" />
        <img src="img/clients/apex-solutions.svg" alt="Apex Solutions" loading="lazy" />
        <!-- Duplicate for seamless loop -->
        <img src="img/clients/marina-bay-hotels.svg" alt="Marina Bay Hotels" loading="lazy" />
        <img src="img/clients/greentech-asia.svg" alt="GreenTech Asia" loading="lazy" />
        <img src="img/clients/nexus-media.svg" alt="Nexus Media" loading="lazy" />
        <img src="img/clients/orbit-tech.svg" alt="Orbit Tech" loading="lazy" />
        <img src="img/clients/pearl-events.svg" alt="Pearl Events" loading="lazy" />
      </div>'''

content = content[:start] + new_section + content[end:]

with open('index.html', 'w') as f:
    f.write(content)

print('Clients section updated successfully')
print('Old section length:', len(old_section))
print('New section length:', len(new_section))
