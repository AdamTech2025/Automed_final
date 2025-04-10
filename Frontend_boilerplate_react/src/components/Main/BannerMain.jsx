import React from "react";
import { useLocation, Link } from "react-router-dom";
import useBreadcrumbs from "use-react-router-breadcrumbs";
import backgroundImage from "../../assets/images/sample.jpg";

// Define the breadcrumb routes
const routes = [
  { path: '/', breadcrumb: 'Home' },
  { path: '/home1', breadcrumb: 'Home1' },
  { path: '/home2', breadcrumb: 'Home2' },
  { path: '/about-company', breadcrumb: 'About Company' },
  { path: '/core-values', breadcrumb: 'Core Values' },
  { path: '/leadership', breadcrumb: 'Leadership' },
  { path: '/history', breadcrumb: 'History' },
  { path: '/services', breadcrumb: 'Services' },
  { path: '/blog-grid', breadcrumb: 'Blog Grid' },
  { path: '/blog-list', breadcrumb: 'Blog List' },
  { path: '/blog-details', breadcrumb: 'Blog Details' },
  { path: '/contact-us', breadcrumb: 'Contact Us' },
  { path: '/services-list', breadcrumb: 'Services List' },
  { path: '/services-details', breadcrumb: 'Service Details' },
  { path: '/project-list', breadcrumb: 'Project List' },
  { path: '/project-grid', breadcrumb: 'Project Grid' },
  { path: '/project-details', breadcrumb: 'Project Details' },
];

const BannerMain = () => {
  const location = useLocation();
  const breadcrumbs = useBreadcrumbs(routes);

  // Get the current breadcrumb to set the title
  const currentBreadcrumb = breadcrumbs[breadcrumbs.length - 1]?.breadcrumb;

  return (
    <div className="relative flex items-center justify-center text-white h-96 bg-gray-800">
      <div
        className="absolute inset-0 w-full h-full bg-cover bg-center"
        style={{ backgroundImage: `url(${backgroundImage})` }}
      ></div>
      <div className="relative z-10 w-full h-full flex flex-col justify-center items-center bg-black bg-opacity-60 p-8">
        <h1 className="text-4xl md:text-5xl lg:text-6xl font-roboto font-bold mb-4 text-center">
          {currentBreadcrumb || 'Default Title'}
        </h1>
        <p className="text-md text-center mb-4 max-w-2xl">
          Our values and vaulted us to the top of our industry.
        </p>
        <nav className="breadcrumbs text-sm text-center">
          <hr className="w-full mb-2 border-gray-400"></hr>
          {breadcrumbs.map(({ match, breadcrumb }) => (
            <span key={match.pathname} className="inline-block">
              <Link
                to={match.pathname}
                className="text-white hover:text-PrimaryColor transition duration-300 ease-in-out"
              >
                {breadcrumb}
              </Link>
              {match.pathname !== location.pathname && (
                <span className="px-2 text-gray-400"> &gt; </span>
              )}
            </span>
          ))}
        </nav>
      </div>
    </div>
  );
};

export default BannerMain;
