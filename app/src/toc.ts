// Sidebar navigation — flat routes (no global PVE|PVP mode toggle).
export interface NavItem {
  path: string;
  label: string;
  group: string;
}

export const NAV: NavItem[] = [
  { path: "/skills", label: "Skills", group: "Reference" },
  { path: "/combos", label: "Combos", group: "Play" },
  { path: "/practice", label: "Practice", group: "Play" },
  { path: "/tricks", label: "Tricks", group: "Play" },
  { path: "/setup-pve", label: "Setup — PvE", group: "Setup" },
  { path: "/setup-pvp", label: "Setup — PvP", group: "Setup" },
  { path: "/dps", label: "DPS — PvE", group: "Reference" },
  { path: "/dps-pvp", label: "DPS — PvP", group: "Reference" },
  { path: "/reference", label: "Reference", group: "Reference" },
  { path: "/r1", label: "R1 AOS", group: "Future" },
];

export const NAV_GROUPS = ["Play", "Setup", "Reference", "Future"];
