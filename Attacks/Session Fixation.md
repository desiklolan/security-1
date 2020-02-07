1. Attacker goes to the website     and the application automatically assigns them a session ID, so that it     can track who the person is.
2. The attacker then sends a     link to their victim that either includes the same session ID as they had,     or with some Javascript that sets the same session ID in their cookie for     the application (that last one requires an XXS vulnerability)
3. The attacker then tricks the     victim into going to that link and logging in, say by telling them that     they have an issue with their account, or some thing similar
4. Once the victim logs in, both     the attacker and the victim have the same session ID, and since the victim     has logged in, the application regards the attacker as being logged in as     well, and they get full access to the victim's account.

  

The Session Fixation error being observed in the LogEvent table is generated when the value stored in the ASP.Net Session does not match the value which has been saved into a cookie when attempting to compare them. These are stored in standard asp.net objects, and do not interact with the cache. Hence the changes to the caching implemented in v10.6 would not affect these.

The framework of the legacy Portal which deals with Session and cookies etc has not been changed in at least the last 3 years since we moved source control to Git. The last change logged around this was in v9.6 when it was moved from SVN to Git. Therefore the change from v10.5 to v10.6.10 would not have had any impact on how the session and cookies are handled by the legacy portal product

The session and cookie storage are maintained though IS, and as UCLA have recently performed a server migration, I would suspect that the IIS configuration has changed and /or updated so that it is handled differently, which could lead to an increase in session fixation errors.

Alternately, it could be caused by anything that would alter the client's assigned session ID, to make it mismatch with the one on the server (see: https://git.starrez.com/projects/SR/repos/starrez/browse/StarNet.StarRez.Web/StarNet.StarRez.Web.Portal/SectionMaster.master.cs#252,263). UCLA could have a security solution that could be causing that.

 

From <https://jira.starrez.com/browse/TECH-9994>