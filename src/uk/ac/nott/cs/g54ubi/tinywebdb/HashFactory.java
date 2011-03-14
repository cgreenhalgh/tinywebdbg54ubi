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

import java.io.UnsupportedEncodingException;
import java.nio.charset.Charset;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.logging.Level;
import java.util.logging.Logger;

/** Make a good hash :-)
 * 
 * @author cmg
 *
 */
public class HashFactory {
	static Logger logger = Logger.getLogger(HashFactory.class.getName());
	/** digest - shared instance */
	static private MessageDigest digest = null;
	/** get digest */
	private static synchronized byte[] getDigestInternal(byte [] data) {
		if (digest==null) {
			try {
				digest = MessageDigest.getInstance("SHA-1");
			} catch (NoSuchAlgorithmException e) {
				logger.log(Level.SEVERE, "Could not get SHA-1 MessageDigest - cannot create key(s)", e);
				return data;
			}
		}
		byte res[] = digest.digest(data);
		return res;
	}
	/** get digest for string */
	public static String getDigest(String text) {
		try {
			return toHex(getDigestInternal(text.getBytes("UTF-8")));
		} catch (UnsupportedEncodingException e) {
			logger.log(Level.SEVERE, "Could not convert text to bytes for digest", e);
			return text.replace("/", "");
		}
	}
	/** bytes to hex */
	public static String toHex(byte bytes[]) {
		StringBuilder sb = new StringBuilder();
		for (int i=0; i<bytes.length; i++) {
			sb.append(nibble((bytes[i] >> 4) & 0xf));
			sb.append(nibble(bytes[i] & 0xf));
		}
		return sb.toString();
	}
	/** nibble to char */
	public static char nibble(int i) {
		if (i<10)
			return (char)('0'+i);
		else 
			return (char)('a'+i-10);
	}

}
