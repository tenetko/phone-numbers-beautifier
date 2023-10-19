import { React, useState } from "react";
import { Layout, Menu } from "antd";
import { Link } from "atomic-router-react";
import { routes } from "../../models/router";
import { TZBPage } from "../../pages/tzb";
import { RemindersPage } from "../../pages/reminders";


export const Sidebar = () => {
    const [isCollapsed, setCollapsed] = useState(true);

    return(
        <Layout.Sider collapsible onCollapse={(collapsed) => setCollapsed(collapsed)}>
        <Menu theme="dark" mode="inline">
          <Menu.Item key="tzb">          
            <Link to={TZBPage.route}>
              <span>TZB</span>
            </Link>
          </Menu.Item>            
  
          <Menu.Item key="reminders">
            <Link to={RemindersPage.route}>
              Reminders
            </Link>
          </Menu.Item>

          {/* <Menu.Item key="os">
            <Link to="/os">
              OS
            </Link>
          </Menu.Item> */}
        </Menu>
      </Layout.Sider>
    );
};