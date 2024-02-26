//Profile for logging in/signing up/looking at stats
//present in 3 main pages
import {
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  MenuDivider,
  Button,
  Avatar,
} from "@chakra-ui/react";
import { ChevronDownIcon } from "@chakra-ui/icons";
import { NavLink } from "react-router-dom";
import { LuLogOut } from "react-icons/lu";

export default function Profile() {
  return (
    <Menu>
      <MenuButton
        as={Button}
        rightIcon={<ChevronDownIcon />}
        leftIcon={
          <Avatar
            size="sm"
            name="John Smith"
            //   src="https://bit.ly/dan-abramov"
          />
        }
      >
        Me
      </MenuButton>
      <MenuList>
        <MenuItem>Option 1</MenuItem>
        <MenuItem>Option 2</MenuItem>
        <MenuDivider />
        <NavLink to="/">
          <MenuItem icon={<LuLogOut />}>Log Out</MenuItem>
        </NavLink>
      </MenuList>
    </Menu>
  );
}
