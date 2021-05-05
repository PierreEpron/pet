import { AppBar, Toolbar,Typography, makeStyles, Button } from "@material-ui/core";
import React from "react";
import { Link as RouterLink } from "react-router-dom";

const headersData = [
  {
    label: "Import",
    href: "/import",
  },
  {
    label: "Export",
    href: "/export",
  },
  {
    label: "Statistiques",
    href: "/Statistiques",
  },
];

const useStyles = makeStyles(() => ({
  header: {
    backgroundColor: "#400CCC",
  },

  logo: {
    fontFamily: "Work Sans, sans-serif",
    fontWeight: 600,
    color: "#FFFEFE",
    textAlign: "left",
  },

  menuButton: {
      fontFamily: "Open Sans, sans-serif",
      fontWeight: 700,
      size: "18px",
      marginLeft: "38px",
   },

  toolbar: {
    display: "flex",
    justifyContent: "space-between",
  },


}));

export default function Header() {
  const { header, logo, menuButton } = useStyles();
  const displayDesktop = () => {
    return (
      // Ne fonctionne pas à vérifier devrait aligné les bouton menu sur la droite.
      // eslint-disable-next-line no-restricted-globals
      <Toolbar className={toolbar}>
        {PetApp_Nancyclotep}
        <div>{getMenuButtons()}</div>
      </Toolbar>
    );
  };

  const PetApp_Nancyclotep = (
    <Typography variant="h6" component="h1" className={logo}>
      PetApp_Nancyclotep
    </Typography>
  );

  const getMenuButtons = () => {
    return headersData.map(({ label, href }) => {
      return (
        <Button
          {...{
            key: label,
            color: "inherit",
            to: href,
            component: RouterLink,
            className: menuButton
          }}
        >
          {label}
        </Button>
      );
    });
  };

  return (
    <header>
      <AppBar className={header}>{displayDesktop()}</AppBar>
    </header>
  );
}