package uk.ac.nott.cs.g54ubi.tinywebdb;

import java.io.IOException;
import java.util.logging.Logger;

import javax.servlet.http.*;

@SuppressWarnings("serial")
public class Tinywebdbg54ubiServlet extends HttpServlet {
	/** logger */
	Logger logger = Logger.getLogger(Tinywebdbg54ubiServlet.class.getName());
	/** post */
	public void doPost(HttpServletRequest req, HttpServletResponse resp)
			throws IOException {
		String tag = req.getParameter("tag");
		String value = req.getParameter("value");
		logger.info("doPost: contextPath="+req.getContextPath()+", pathInfo="+req.getPathInfo()+", queryString="+req.getQueryString()+", tag="+tag+", value="+value);
		resp.setContentType("application/json");
		resp.getWriter().println("[]");
	}
}
