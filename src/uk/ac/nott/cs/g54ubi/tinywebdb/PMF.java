/**
 * Copyright 2010 The University of Nottingham
 * 
 * This file is part of tinywebdbg54ubi.
 *
 *  tinywebdbg54ubi is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU Affero General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  tinywebdbg54ubi is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU Affero General Public License for more details.
 *
 *  You should have received a copy of the GNU Affero General Public License
 *  along with tinywebdbg54ubi.  If not, see <http://www.gnu.org/licenses/>.
 * 
 */
package uk.ac.nott.cs.g54ubi.tinywebdb;
import javax.jdo.JDOHelper;
import javax.jdo.PersistenceManagerFactory;

/** JDO persistence manager factory
 * @author cmg
 *
 */
public class PMF {
    private static final PersistenceManagerFactory pmfInstance =
        JDOHelper.getPersistenceManagerFactory("transactions-optional");

    private PMF() {}

    public static PersistenceManagerFactory get() {
        return pmfInstance;
    }
}
