import { React, useState } from "react";
import { Layout, Menu } from "antd";
import { Link } from "atomic-router-react";
import { routes } from "../../models/router";
import { TZBPage } from "../../pages/tzb";
import { OSPage } from "../../pages/os";
import { RemindersPage } from "../../pages/reminders";


export const Sidebar = () => {
    const [isCollapsed, setCollapsed] = useState(true);

    return(
        <Layout.Sider collapsible onCollapse={(collapsed) => setCollapsed(collapsed)}>        
        <Menu theme="dark" mode="inline">
          <Menu.Item key="tzb" style={{textAlign: "right"}}>
            <Link to={TZBPage.route}>
              <span>TZB</span>            
            </Link>
          </Menu.Item>
  
          <Menu.Item key="reminders" style={{textAlign: "right"}}>
            <Link to={RemindersPage.route}>
              Reminders            
            </Link>
          </Menu.Item>
          
          <Menu.Item key="os" style={{textAlign: "right"}}>
            <Link to={OSPage.route}>
              OS
            </Link>
          </Menu.Item>
        </Menu>
      </Layout.Sider>
    );
};