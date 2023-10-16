"""IPv4, IPv6 subnets, routes, summaries and its properties, definitions.
"""

from collections import OrderedDict

from nettoolkit_common.gpl import STR, LST, IO

# from errors import incorrectinput
incorrectinput = 'INCORRECT SUBNET OR SUBNET MASK DETECTED NULL RETURNED'

# ----------------------------------------------------------------------------
# Module Functions
# ----------------------------------------------------------------------------

def expand(v6subnet):
	"""Expand the V6 subnet to its full length.

	Args:
		v6subnet (str): zipped v6 subnet

	Returns:
		str: expanded v6 subnet
	"""	
	# try:
	p = ''
	sip = v6subnet.split("/")[0].split("::")
	if len(sip) == 2:
		# ~~~~~~ No padding, inserting zeros in middle ~~~~~~~
		for x in range(1, 9):
			p = STR.string_concate(p, get_hext(v6subnet, hexTnum=x), conj=':')
		v6subnet = p
	else :
		# ~~~~~~~ pad leading zeros ~~~~~~~
		lsip = sip[0].split(":")
		for x in range(8-len(lsip), 0, -1):
			p = STR.string_concate(p, '0', conj=":")
		if p != '':
			v6subnet = p + ':' + v6subnet
	return v6subnet
	# except:
	# 	return False

def get_hext(v6subnet, hexTnum, s=''):	
	"""get the a hextate of v6 subnet.

	Args:
		v6subnet (str): v6 subnet string
		hexTnum (int): hextate number

	Raises:
		Exception: Raise Exception if incorrect input

	Returns:
		str: hextate string
	"""	
	test = hexTnum == 1
	if s == '':
		s = v6subnet.split("/")[0]
	try:
		if s != '' and all([hexTnum>0, hexTnum<=8]):
			sip = s.split("/")[0].split("::")
			# if test: print(hexTnum, s)
			lsip = sip[0].split(":")
			if hexTnum <= len(lsip):
				lsiphext = lsip[hexTnum-1]
				if lsiphext: return lsip[hexTnum-1]
				return '0'
			else:
				rsip = sip[1].split(":")
				if rsip[0] == '': rsip = []
				if 8-hexTnum < len(rsip):
					# if test: print(">>", rsip[(9-hexTnum)*-1])
					return rsip[(9-hexTnum)*-1]
				else:
					# if test: print(">>> 0", )
					return '0'
		else:
			raise Exception(incorrectinput)
			return None
	except:
		raise Exception(incorrectinput)
		return None


def bin_mask(mask):
	"""mask representation in binary (ex: 255.255.255.0)

	Args:
		mask (int): mask in number 

	Returns:
		str: mask in 8 byte format
	"""    	
	mask = int(mask)
	decmask = mask*str(1) + (32-mask)*str(0)
	o1 = str(int(decmask[ 0: 8] , 2))
	o2 = str(int(decmask[ 8: 16], 2))
	o3 = str(int(decmask[16: 24], 2))
	o4 = str(int(decmask[24: 32], 2))
	return o1+'.'+o2+'.'+o3+'.'+o4	


def invmask_to_mask(invmask):
	m = binsubnet(invmask)
	return 32 - m.count("1")


def _invalid_subnet(subnet): 
	"""invalid subnet str
	"""	
	return f"Not a VALID Subnet {subnet}"


def to_dec_mask(dotted_mask):
	"""Decimal mask representation

	Args:
		dotted_mask (str): input mask = dotted mask

	Returns:
		int: mask
	"""    	
	return bin2decmask(binsubnet(dotted_mask))


def bin2dec(binnet): 
	"""Decimal network representation / integer value

	Args:
		binnet (str): input = dotted network

	Returns:
		int: decimal number of network
	"""	
	if not binnet: return 0
	return int(binnet, 2)


def bin2decmask(binmask):
	"""Decimal mask representation / integer value

	Args:
		binmask (str): input mask = binary mask in number

	Returns:
		int: mask
	"""    	
	return binmask.count('1')


def binsubnet(subnet):
	"""convert subnet to binary:0s and 1s

	Args:
		subnet (str): subnet string (v4, v6)

	Returns:
		str: binary subnet representation ( 0s and 1s )
	"""    	
	try:
		if STR.found(subnet, "."): version, split_by, bit_per_oct = 4, ".", 8
		if STR.found(subnet, ":"): version, split_by, bit_per_oct = 6, ":", 16
		s = ''
		octs = subnet.split("/")[0].split(split_by)
		for o in octs:
			if version == 4:
				bo = str(bin(int(o)))[2:]
			elif version == 6:
				bo = str(bin(int(o, bit_per_oct)))[2:]
			lbo = len(bo)
			pzero = '0'*(bit_per_oct - lbo)
			s = s + pzero + bo
		return s
	except:
		pass


def addressing(subnet):
	"""proives ip-subnet object for various functions on it

	Args:
		subnet (str): either ipv4 or ipv6 subnet with /mask

	Returns:
		IPv4, IPv6: IPv4 or IPv6 object
	"""    	
	v_obj = Validation(subnet)
	if v_obj.validated: return v_obj.ip_obj


def get_summaries(*net_list):
	"""summarize the provided network prefixes, provide all networks as arguments.

	Returns:
		list: summaries
	"""    	
	if not isinstance(net_list, (list, tuple, set)): return None
	s = Summary(*net_list)
	s.calculate()
	summaries = s.prefixes
	i = 0	
	while True:
		i += 1
		if i >= MAX_RECURSION_DEPTH: break
		ss = Summary(*summaries)
		ss.calculate()
		if summaries == ss.prefixes: break
		summaries = ss.prefixes
	return sorted(summaries)


def isSplittedRoute(line):
	"""checks if ip route is splitted in multiple lines or not.

	Args:
		line (str): ip route line from configuration

	Returns:
		int: 1: No single line,  0 : Yes splitted line [line1],  -1: Yes splitted line [line2]
	"""    	
	if STR.found(line, ','):
		return 1 if len(line.split()) > 5 else -1
	else:
		return 0

def isSubset(pfx, supernet):
	"""Check if provided prefix is part of provided supernet or not.

	Args:
		pfx (str): subnet
		supernet (str): supernet

	Raises:
		Exception: if an input error occur

	Returns:
		bool: True if subnet is part of supernet else False
	"""    	
	if not isinstance(pfx, (str, IPv4)):
		raise Exception("INPUTERROR")
	if not isinstance(supernet, (str, IPv4)):
		raise Exception("INPUTERROR")
	if isinstance(supernet, str): supernet = addressing(supernet)
	if isinstance(pfx, str): pfx = addressing(pfx)
	if supernet.mask <= pfx.mask:
		supernet_bin = binsubnet(supernet.subnet)
		pfx_bin = binsubnet(pfx.subnet)
		if supernet_bin[0:supernet.mask] == pfx_bin[0:supernet.mask]:
			return True
	return False	


# ----------------------------------------------------------------------------
# Validation Class - doing subnet validation and version detection
# ----------------------------------------------------------------------------
class Validation():
	"""ip-subnet validation class, provide ipv4 or ipv6 subnet with "/" mask
	"""    	

	def __init__(self, subnet):
		"""Initialise the validation.

		Args:
			subnet (str): ipv4 or ipv6 subnet with "/" mask
		"""    		
		self.mask = None
		self.subnet = subnet
		self.version = self._version()
		self.validated = False
		self._check_ip_object()


	def _version(self):
		"""ip version number

		Returns:
			int: version number
		"""    		
		if STR.found(self.subnet, ":"):
			return 6
		elif STR.found(self.subnet, "."):
			return 4
		else:
			return 0

	def _check_ip_object(self):
		"""internal checking method

		Raises:
			Exception: _description_

		Returns:
			_type_: _description_
		"""    		
		object_map = {4: IPv4, 6: IPv6}
		func_map = {4: self.check_v4_input, 6: self.check_v6_input}
		if self.version in object_map:
			self.validated = func_map[self.version]()
			if not self.validated: return None
			self.ip_obj = object_map[self.version](self.subnet)
			self.validated = expand(self.ip_obj + 0) == expand(self.ip_obj.NetworkIP(False))

			if not self.validated:  return None
		else:
			raise Exception(_invalid_subnet(self.subnet))

	def check_v4_input(self):
		'''validation of v4 subnet
		'''
		# ~~~~~~~~~ Mask Check ~~~~~~~~~
		try:
			self.mask = self.subnet.split("/")[1]
		except:
			self.mask = 32
			self.subnet = self.subnet + "/32"
		try:			
			self.mask = int(self.mask)
			if not all([self.mask>=0, self.mask<=32]):
				raise Exception(f"Invalid mask length {self.mask}")
		except:
			raise Exception(f"Incorrect Mask {self.mask}")

		# ~~~~~~~~~ Subnet Check ~~~~~~~~~
		try:
			octs = self.subnet.split("/")[0].split(".")
			if len(octs) != 4:
				raise Exception(f"Invalid Subnet Length {len(octs)}")
			for i in range(4):
				if not all([int(octs[i])>=0, int(octs[i])<=255 ]):
					raise Exception(f"Invalid Subnet Octet {i}")
			return True
		except:
			raise Exception(f"Unidentified Subnet: {self.subnet}")

	def check_v6_input(self):
		'''validation of v6 subnet
		'''
		try:
			# ~~~~~~~~~ Mask Check ~~~~~~~~~
			self.mask = self.subnet.split("/")[1]
		except:
			self.mask = 128
			self.subnet = self.subnet + "/128"
		try:
			self.mask = int(self.mask)
			if not all([self.mask>=0, self.mask<=128]):
				raise Exception(f"Invalid mask length {self.mask}")
			
			# ~~~~~~~~~ Subnet ~~~~~~~~~
			sip = self.subnet.split("/")[0].split("::")
			
			# ~~~~~~~~~ Check Subnet squeezers ~~~~~~~~~
			if len(sip) > 2:
				raise Exception("Invalid Subnet, Squeezers detected > 1")
			
			# ~~~~~~~~~ Subnet Length ~~~~~~~~~
			lsip = sip[0].split(":")
			try:
				rsip = sip[1].split(":")
			except:
				rsip = []
			if len(lsip)+len(rsip) > 8:
				raise Exception(f"Invalid Subnet Length {len(lsip)+len(rsip)}")
			
			# ~~~~~~~~~ Validate Hextates ~~~~~~~~~
			for hxt in lsip+rsip:
				try:
					if hxt != '' :
						hex(int(hxt, 16))
				except:
					raise Exception(f"Invalid Hextate {hxt}")
			
			# ~~~~~~~~~ All Good ~~~~~~~~~
			return True

		except:
			raise Exception("Unidentified Subnet")

# --------------------------------------------------------------------------------------------------
# Parent IP class defining default methods for v4 and v6 objects
# --------------------------------------------------------------------------------------------------

class IP():
	"""defines common properties and methods for IPV4 and IPV6 Objects
	"""
	def __init__(self, subnet):
		self.subnet = subnet
		self.mask = int(self.subnet.split("/")[1])
		self.net = self.subnet.split("/")[0]
	def __hash__(self):
		try:
			return bin2dec(binsubnet(self.NetworkIP()))
		except:
			raise Exception(f"UnhashableInput: {self.subnet}")
	def __str__(self): return self.subnet
	def __repr__(self): return self.subnet
	def __len__(self): 
		if self.version == 4: 
			return bin2dec(binsubnet(self.broadcast_address())) - bin2dec(binsubnet(self.subnet_zero())) + 1
		if self.version == 6:
			raise Exception("Excessive Integer Value Assignment not possible. "
				"Use IPv6.len() method to get the length of object"
				)
	def __gt__(self, ip): return bin2dec(binsubnet(self.NetworkIP())) - bin2dec(binsubnet(ip.broadcast_address())) > 0
	def __lt__(self, ip): return bin2dec(binsubnet(self.NetworkIP())) - bin2dec(binsubnet(ip.broadcast_address())) < 0
	def __eq__(self, ip): return bin2dec(binsubnet(self.NetworkIP())) - bin2dec(binsubnet(ip.broadcast_address())) == 0
	def __add__(self, n):
		'''add n-ip's to given subnet and return udpated subnet'''
		if isinstance(n, int):
			return self.n_thIP(n, False, "_")
		elif isinstance(n, IPv4):
			summary = get_summaries(self, n)
			if len(summary) == 1:
				return get_summaries(self, n)[0]
			else:
				raise Exception(
					"Inconsistant subnets cannot be added "
					"and >2 instances of IPv4/IPv6 Object add not allowed. please check inputs or "
					"Use 'get_summaries' function instead"
					)
	def __sub__(self, n): return self.n_thIP(-1*n, False, "_")
	def __truediv__(self, n): return self._sub_subnets(n)
	def __iter__(self): return self._subnetips()
	def __getitem__(self, n):
		try:
			return self.n_thIP(n, False)
		except:
			l = []
			for x in self._subnetips(n.start, n.stop):
				l.append(x)
			return tuple(l)
	def __contains__(self, pfx): isSubset(pfx, self)

	# get n-number of subnets of given super-net
	def _sub_subnets(self, n):
		_iplst = []
		for i1, x1 in enumerate(range(self.bit_length)):
			p = 2**x1
			if p >= n: break
		_nsm = self.mask + i1
		_nip = int(binsubnet(self.subnet_zero()), 2)
		_bcip = int(binsubnet(self.broadcast_address()), 2)
		_iis = (_bcip - _nip + 1) // p
		for i2, x2 in enumerate(range(_nip, _bcip, _iis)):
			_iplst.append(self.n_thIP(i2*_iis)+ "/" + str(_nsm))
		return tuple(_iplst)

	# yields IP Address(es) of the provided subnet
	def _subnetips(self, begin=0, end=0):
		_nip = int(binsubnet(self.subnet_zero()), 2)
		if end == 0:
			_bcip = int(binsubnet(self.broadcast_address()), 2)
		else:
			_bcip = _nip + (end-begin)
		for i2, x2 in enumerate(range(_nip, _bcip)):
			if begin>0:  i2 = i2+begin
			yield self.n_thIP(i2)



# ----------------------------------------------------------------------------
# IP Subnet (IPv6) class 
# ----------------------------------------------------------------------------

class IPv6(IP):
	'''IPv6 object
	'''

	version = 6
	bit_length = 128

	# Object Initializer
	def __init__(self, subnet=''):
		"""initialize the IPv6 object for provided v6 subnet

		Args:
			subnet (str): ipv6 subnet with mask.
		"""    		
		super().__init__(subnet)
		self._network_ip()
		self.__actualv6subnet = False				# breaked subnet expanded
		self._network_address_bool = False			# Subnet zero available/not

	def len(self): 
		"""Subnet size

		Returns:
			int: count of ip in this subnet 
		"""	
		return bin2dec(binsubnet(self.broadcast_address())) - bin2dec(binsubnet(self.subnet_zero())) + 1

	# ------------------------------------------------------------------------
	# Private Methods
	# ------------------------------------------------------------------------

	# update Subnet to actual length / expand zeros 
	def _to_actualsize(self):
		self.subnet = expand(self.subnet)
		# if not self.subnet: return False
		return self.subnet

	# update Subnet to actual length / expand zeros 
	# def _to_actualsize(self):		
	# 	try:
	# 		if not self.__actualv6subnet:
	# 			p = ''
	# 			sip = self.subnet.split("/")[0].split("::")
	# 			if len(sip) == 2:
	# 				# ~~~~~~ No padding, inserting zeros in middle ~~~~~~~
	# 				for x in range(1, 9):
	# 					p = STR.string_concate(p, self._get_hext(hexTnum=x), conj=':')
	# 				self.subnet = p
	# 			else :
	# 				# ~~~~~~~ pad leading zeros ~~~~~~~
	# 				lsip = sip[0].split(":")
	# 				for x in range(8-len(lsip), 0, -1):
	# 					p = STR.string_concate(p, '0', conj=":")
	# 				if p != '':
	# 					self.subnet = p + ':' + self.subnet
	# 			self.__actualv6subnet = True
	# 	except:
	# 		return False

	# IP Portion of Input
	def _network_ip(self):
		try:
			self.network = self.subnet.split("/")[0]
			return self.network
		except:
			raise Exception(f"NoValidIPv6SubnetDetected: {self.subnet}")
			return None

	# Padding subnet with ":0" or ":ffff"
	@staticmethod
	def _pad(padwhat='0', counts=0):
		s = ''
		for x in range(counts):
			s = s + ":" + padwhat
		return s

	# Return a specific Hextate (hexTnum) from IPV6 address
	def _get_hext(self, hexTnum, s=''):	return get_hext(self.subnet, hexTnum, s)

	# Return a specific Hextate (hexTnum) from IPV6 address
	# def _get_hext(self, hexTnum, s=''):	
	# 	test = hexTnum == 1
	# 	if s == '':
	# 		s = self.subnet.split("/")[0]
	# 	try:
	# 		if s != '' and all([hexTnum>0, hexTnum<=8]):
	# 			sip = s.split("/")[0].split("::")
	# 			# if test: print(hexTnum, s)
	# 			lsip = sip[0].split(":")
	# 			if hexTnum <= len(lsip):
	# 				lsiphext = lsip[hexTnum-1]
	# 				if lsiphext: return lsip[hexTnum-1]
	# 				return '0'
	# 			else:
	# 				rsip = sip[1].split(":")
	# 				if rsip[0] == '': rsip = []
	# 				if 8-hexTnum < len(rsip):
	# 					# if test: print(">>", rsip[(9-hexTnum)*-1])
	# 					return rsip[(9-hexTnum)*-1]
	# 				else:
	# 					# if test: print(">>> 0", )
	# 					return '0'
	# 		else:
	# 			raise Exception(incorrectinput)
	# 			return None
	# 	except:
	# 		raise Exception(incorrectinput)
	# 		return None

	# Return Number of Network Hextates (hxts) from IPV6 address
	def _get_hextates(self, hxts=1, s=''):
		ox = ''
		for o in range(1, hxts+1):
			ox = STR.string_concate(ox, self._get_hext(o, s=s), conj=':')
		return ox+":"

	# NETWORK / BC Address Calculation : addtype = 'NET' , 'BC'
	def _endpoint(self, addtype='NET'):
		self._to_actualsize()
		if self.mask != '' and self.mask<128:	 # Non host-only subnets
			x = 0 if addtype == 'NET' else -1
			padIP = '0' if addtype == 'NET' else 'ffff'
			(asilast, avs) = ([], [])
			fixedOctets = self.mask//16

			## get full list of available subnets in selected Hexate.
			while x < 65536:	
				asilast.append(x)
				x = x + (2**(16-(self.mask-((fixedOctets)*16))))

			## check avlbl subnet and choose less then given one.
			for netx in asilast:		
				avs.append(self._get_hextates(fixedOctets)  
										+ str(hex(netx))[2:])
				if addtype =='BC':
					last_subnet = avs[-1]
				if int(self._get_hext(fixedOctets+1), 16) < netx:
					break
				if addtype =='NET':
					last_subnet = avs[-1]

			## Return subnet by padding zeros.
			self.fixedOctets = fixedOctets
			nt = last_subnet+self._pad(padIP, 7-fixedOctets)
			if nt[0] == ":": nt = nt[1:]
			return nt

		else:									# host-only subnet
			return self.network

	def _add_ip_to_network_address(self, num=0, _=''):
		'''-->Adds num of IP to Network IP and return address'''
		self._network_address
		s = self._subnet_zero
		if _ != '':
			s = self.subnet
		_7o = self._get_hextates(7, s)
		_8o = int(self._get_hext(8, s), 16) + num
		return _7o + str(hex(_8o)[2:])

	@property
	def _broadcast_address(self): return self._endpoint(addtype='BC')
	@property
	def _network_address(self):
		'''-->Returns only NETWORK ADDRESS for given subnet'''
		if not self._network_address_bool:
			self._subnet_zero = self._endpoint(addtype='NET')
			self._network_address_bool = True
		return self._subnet_zero
	NetworkAddress = _network_address


	# ------------------------------------------------------------------------
	# Public Methods 
	# ------------------------------------------------------------------------

	def get_hext(self, hexTnum): 
		"""get a specific Hextate value from IPV6 address
		same as: getHext

		Args:
			hexTnum (int): hextate number

		Returns:
			str: hextate value
		"""		
		return self._get_hext(hexTnum)
	getHext = get_hext

	def subnet_zero(self, withMask=True):
		"""Network Address (subnet zero) with/without mask for given subnet
		same as: NetworkIP

		Args:
			withMask (bool, optional): return with mask. Defaults to True.

		Returns:
			str: Network Address
		"""    		
		if withMask :
			return self._network_address + "/" + str(self.mask)
		else:
			return self._network_address
	NetworkIP = subnet_zero

	def broadcast_address(self, withMask=True):
		"""Broadcast Address with/without mask for given subnet
		same as: BroadcastIP

		Args:
			withMask (bool, optional): return with mask. Defaults to True.

		Returns:
			str: Broadcast Address
		"""
		if withMask :
			return self._broadcast_address + "/" + str(self.mask)
		else:
			return self._broadcast_address
	BroadcastIP = broadcast_address

	def n_thIP(self, n=0, withMask=False, _=''):
		"""n-th IP with/without mask from given subnet

		Args:
			n (int, optional): n-th ip. Defaults to 0.
			withMask (bool, optional): return with mask. Defaults to False.

		Returns:
			str: nth IP Address string
		"""
		ip = self._add_ip_to_network_address(n, _)
		mask = self.decimalMask
		return ip+"/"+mask if withMask else ip

	@property
	def decimalMask(self):
		'''decimal mask of given subnet
		same as: decmask
		'''
		return str(self.mask)
	decmask = decimalMask

	## - NA - for IPv6 ##
	@property
	def binmask(self): 
		"""Not Implemented for IPv6 """		
		return None
	@property
	def invmask(self): 
		"""Not Implemented for IPv6 """		
		return None
	def ipdecmask(self, n=0): 
		"""nth ip with decimal mask"""
		return self.n_thIP(n, True)
	def ipbinmask(self, n=0): 
		"""Not Implemented for IPv6 """		
		return None
	def ipinvmask(self, n=0): 
		"""Not Implemented for IPv6 """		
		return None


# ----------------------------------------------------------------------------
# IPv4 Subnet (IPv4) class 
# ----------------------------------------------------------------------------
class IPv4(IP):
	'''IPv4 object
	'''

	version = 4
	bit_length = 32

	# ------------------------------------------------------------------------
	# Private methods / Properties
	# ------------------------------------------------------------------------

	# binary mask return property
	@property
	def _binmask(self):
		try:
			pone ='1'*self.mask
			pzero = '0'*(32-self.mask)
			return pone+pzero
		except:
			pass

	# Inverse mask return property
	@property
	def _invmask(self):
		try:
			pone ='0'*self.mask
			pzero = '1'*(32-self.mask)
			return pone+pzero
		except:
			pass

	@staticmethod
	def _pad_zeros(bins): 
		return '0'*(34 - len(str(bins)))+bins[2:]
	@staticmethod
	def _octets_bin2dec(binnet): 
		return  [bin2dec(binnet[x:x+8]) for x in range(0, 32, 8) ]
	def _bin_and(self, binone, bintwo):
		return self._pad_zeros(bin(int(binone.encode('ascii'), 2) & int(bintwo.encode('ascii'), 2) ))
	def _bin_or(self, binone, bintwo):
		return self._pad_zeros(bin(int(binone.encode('ascii'), 2) | int(bintwo.encode('ascii'), 2) ))

	# ------------------------------------------------------------------------
	# Available Methods & Public properties of class
	# ------------------------------------------------------------------------

	def subnet_zero(self, withMask=True):
		"""Network IP Address (subnet zero) of subnet from provided IP/Subnet.
		same as: NetworkIP

		Args:
			withMask (bool, optional): return with mask. Defaults to True.

		Returns:
			str: Network address
		"""    		
		try:
			s = binsubnet(self.subnet)
			bm = self._binmask
			net = LST.list_to_octet(self._octets_bin2dec(self._bin_and(s, bm )))
			if withMask :
				return net + "/" + str(self.mask)
			else:
				return net
		except:
			pass
	NetworkIP = subnet_zero

	def broadcast_address(self, withMask=False):
		"""Broadcast IP Address of subnet from provided IP/Subnet
		same as: BroadcastIP

		Args:
			withMask (bool, optional): return with mask. Defaults to False.

		Returns:
			str: broadcast ip
		"""    		
		try:
			s = binsubnet(self.subnet)
			im = self._invmask
			bc = LST.list_to_octet(self._octets_bin2dec(self._bin_or(s, im )))
			if withMask :
				return bc + "/" + str(self.mask)
			else:
				return bc
		except:
			pass
	BroadcastIP = broadcast_address

	def n_thIP(self, n=0, withMask=False, _='', summary_calc=False):
		"""n-th IP Address of subnet from provided IP/Subnet

		Args:
			n (int, optional): number of ip. Defaults to 0.
			withMask (bool, optional): return with mask. Defaults to False.

		Raises:
			Exception: for address out of range

		Returns:
			str: nth ip address
		"""
		s = binsubnet(self.subnet)
		if _ == '':
			bm = self._binmask
			addedbin = self._pad_zeros(bin(int(self._bin_and(s, bm), 2)+n))
		else:
			addedbin = self._pad_zeros(bin(int(s.encode('ascii'), 2 )+n))

		if (any([addedbin > binsubnet(self.broadcast_address()), 
				addedbin < binsubnet(self.NetworkIP())]) and 
			not summary_calc
			):
			raise Exception("Address Out of Range")

		else:
			ip = LST.list_to_octet(self._octets_bin2dec(addedbin))
			if withMask :
				return ip + "/" + str(self.mask)
			else:
				return ip

	@property
	def decmask(self):
		'''Decimal Mask from provided IP/Subnet - Numeric/Integer'''
		return self.mask
	decimalMask = decmask

	@property
	def binmask(self):
		'''Binary Mask from provided IP/Subnet'''
		return LST.list_to_octet(self._octets_bin2dec(self._binmask))

	@property
	def invmask(self):
		'''Inverse Mask from provided IP/Subnet'''
		return LST.list_to_octet(self._octets_bin2dec(self._invmask))

	def ipdecmask(self, n=0):
		"""IP with Decimal Mask for provided IP/Subnet,

		Args:
			n (int, optional): n-th ip of subnet will appear in output if provided. Defaults to 0.

		Raises:
			Exception: invalid input

		Returns:
			str: ipaddress/mask
		"""    		
		try:
			return self[n] + "/" + str(self.mask)
		except:
			raise Exception(f'Invalid Input : detected')

	def ipbinmask(self, n=0):
		"""IP with Binary Mask for provided IP/Subnet,

		Args:
			n (int, optional): n-th ip of subnet will appear in output if provided,. Defaults to 0.

		Raises:
			Exception: invalid input

		Returns:
			str: ip_address subnet_mask
		"""    		
		try:
			return self[n] + " " + self.binmask
		except:
			raise Exception(f'Invalid Input : detected')

	def ipinvmask(self, n=0):
		"""IP with Inverse Mask for provided IP/Subnet,

		Args:
			n (int, optional): n-th ip of subnet will appear in output if provided. Defaults to 0.

		Raises:
			Exception: invalid input

		Returns:
			str: ip_address inverse_mask
		"""    		
		try:
			return self[n] + " " + self.invmask
		except:
			raise Exception(f'Invalid Input : detected')



# ------------------------------------------------------------------------------
# Routes Class
# ------------------------------------------------------------------------------
class Routes(object):
	"""Routes Object
	"""    	


	def __init__(self, hostname, route_list=None, route_file=None):
		"""Initialize Route object
		Either one input is require (route_list, route_file)

		Args:
			hostname (str): device hostname
			route_list (list, optional): cisco sh route command in list format. Defaults to None.
			route_file (str, optional): text file of sh route output. Defaults to None.
		"""    		
		if route_file != None: route_list = IO.file_to_list(route_file)
		self.__parse(route_list, hostname)

	def __getitem__(self, key):
		return self.routes[key]

	def __iter__(self):
		for k, v in self.routes.items():
			yield (k, v)

	@property
	def reversed_table(self):
		"""reversed routes

		Yields:
			tuple: route, route_attributes
		"""
		for k, v in reversed(self.routes.items()):
			yield (k, v)

	@property
	def routes(self):
		"""routes with its name"""
		return self._op_items

	def get_prefix_desc(self, prefix):
		"""prefix description if available or returns it for default route

		Args:
			prefix (str): prefix to check

		Raises:
			Exception: input error

		Returns:
			str: prefix remark/description if any
		"""    		
		pfxlst = []
		if isinstance(prefix, str):
			x = self.__check_in_table(addressing(prefix))[1]
			try:
				pfxlst.append(self[x])
				return pfxlst[0]
			except:
				print("prefixesNotinAnySubnet: Error")
				return None
		elif isinstance(prefix, IPv4):
			x = self.__check_in_table(prefix.subnet)
			pfxlst.append(self[x])
		elif isinstance(prefix, (list, tuple, set)):
			for p in prefix:
				px = self.get_prefix_desc(p)
				if px:
					pfxlst.append(px)
		else:
			raise Exception("INPUTERROR")
		if len(set(pfxlst)) == 1:
			return pfxlst[0]
		else:
			print("prefixesNotinSamesubnet: Error")

	def inTable(self, prefix):
		"""check if prefix is in routes table, return for default-route otherwise

		Args:
			prefix (str): prefix to check

		Returns:
			bool: prefix in table or not
		"""    		
		return self.__check_in_table(prefix)[0]

	def outerPrefix(self, prefix):
		"""check and return parent subnet of prefix in routes table, default-route otherwise

		Args:
			prefix (str): prefix to check

		Returns:
			str: matching prefix/supernet
		"""    		
		return self.__check_in_table(prefix)[1]

	######################### LOCAL FUNCTIONS #########################

	# Helper for inTable and outerPrefix
	def __check_in_table(self, prefix):
		if not isinstance(prefix, (str, IPv4)):
			raise Exception("INPUTERROR")
		for k, v in self.reversed_table:
			if k == '0.0.0.0/0': continue
			if isSubset(prefix, k):
				return (True, k)
				break
		return (False, '0.0.0.0/0')

	# set routes in dictionary/ parser
	def __parse(self, route_list, hostname):
		headers = (
		"L - local", "C - connected", "S - static", "R - RIP", "M - mobile", "B - BGP",
		"D - EIGRP", "EX - EIGRP external", "O - OSPF", "IA - OSPF inter area", 
		"N1 - OSPF NSSA external type 1", "N2 - OSPF NSSA external type 2",
		"E1 - OSPF external type 1", "E2 - OSPF external type 2", "V - VPN",
		"i - IS-IS", "su - IS-IS summary", "L1 - IS-IS level-1", "L2 - IS-IS level-2",
		"ia - IS-IS inter area", "* - candidate default", "U - per-user static route",
		"o - ODR", "P - periodic downloaded static route", "+ - replicated route",
		"Gateway of last resort"
		)
		op_items = OrderedDict()
		for line in route_list:
			if STR.is_blank_line(line): continue
			if STR.is_hostname_line(line, hostname): continue
			if STR.find_any(line, headers): continue
			if isSplittedRoute(line) == 0:
				spl = line.strip()
				continue
			if isSplittedRoute(line) == -1:
				line = spl + ' ' + line
			spl = line.split(",")
			if line.find('0.0.0.0 0.0.0.0') > -1:
				op_items['0.0.0.0/0'] = STR.replace_dual_and_split(spl[1])[-1].strip()
				continue
			route = STR.replace_dual_and_split(spl[0])[1]
			try:
				routeMask = binsubnet(STR.replace_dual_and_split(spl[0])[2]).count('1')
			except:
				print(spl)
			routeDesc = STR.replace_dual_and_split(spl[-1])[-1]
			op_items[route + '/' + str(routeMask)] = routeDesc.strip()
		self._op_items = op_items


# ----------------------------------------------------------------------------
# Prefixes summarization class 
# ----------------------------------------------------------------------------

MAX_RECURSION_DEPTH = 100		# default recursion depth, increase if exceeding and need to go deep more.
class Summary(IPv4):
	'''Defines Summaries of prefixes
	'''

	def __init__(self, *args):		
		"""initialize object with provided args=prefixes
		"""		
		self.networks = set()
		for arg in args:
			if isinstance(arg, str):
				if arg.strip():
					arg=IPv4(arg)
			self.networks.add(arg)
		self.summaries = []
		self.networks = sorted(self.networks)
		self._validate_and_update_networks()

	@property
	def prefixes(self):
		"""set of summary addresses

		Returns:
			set: summaries
		"""    		
		for pfx in self.summaries:
			if isinstance(pfx, str): pfx = IPv4(pfx)
		return set(self.summaries)

	# provided networks validation, remove non-validated networks.
	def _validate_and_update_networks(self):
		for network in self.networks:
			if not Validation(str(network)).validated:
				print(f"InvalidSubnetDetected-Removed: {network}")
				self.networks.remove(network)

	# kick
	def calculate(self):
		"""calculate summaries for provided networks
		"""
		prev_network = None
		for network in self.networks:
			_sumy = self.summary(prev_network, network)
			prev_network = _sumy if _sumy is not None else network
			if _sumy is not None: 
				if isinstance(prev_network, str): 
					_sumy = IPv4(_sumy)
					prev_network = IPv4(prev_network)
				self.summaries.append(_sumy)
			else:
				self.summaries.append(network)
				continue

	def summary(self, s1, s2):
		"""summary of given two network addresses s1 and s2
		"""
		if s2 is None: return s1
		if s1 is None: return s2
		if self._are_equal(s1, s2): return s1
		big_subnet = self._is_any_subset(s1, s2)
		if big_subnet: return big_subnet
		self._sequnce_it(s1, s2)
		self._local_vars()
		if not self._contigious() or not self._immidiate(): return None
		summary_ip = self.first.NetworkIP(False)+"/"+str(self.mask)
		return summary_ip if Validation(summary_ip).validated else None

	# Order the subnet sequencially.
	def _sequnce_it(self, s1, s2):
		if int(binsubnet(s1.NetworkIP()), 2 ) > int(binsubnet(s2.NetworkIP()), 2 ):
			(first, second) = (s2, s1) 
		else: 
			(first, second) = (s1, s2)
		self.first, self.second = first, second

	# defining some local variables
	def _local_vars(self):
		# ---------- set local vars ------------------
		self.first_len = len(self.first)
		self.second_len = len(self.second)	
		self.total = 2*self.first_len if self.first_len >= self.second_len else 2*self.second_len
		self.mask = 32 - len(bin(self.total-1)[2:])			# tantative summary mask
		# --------------------------------------------

	# are provided two prefixes equal or not, check boolean
	def _are_equal(self, s1, s2): return s1.mask == s2.mask and s1.NetworkIP() == s2.NetworkIP()

	# is s1 part of s2 ?
	def _is_any_subset(self, s1, s2):
		(big_subnet, small_subnet) = (s2, s1) if s1.mask > s2.mask else (s1, s2)
		is_part = False
		for power in range(1, 33):
			no_of_subnets = (2**power)
			try:
				portions = big_subnet/no_of_subnets
			except ValueError:
				break
			if small_subnet.NetworkIP() in portions:
				is_part = True
				break
		return big_subnet if is_part else None

	# a condition
	def _contigious(self):
		# condition 1 - next ip of subnet 1 should be network ip of subnet 2 / Verfications
		return self.first.n_thIP(self.first_len, summary_calc=True) == self.second.NetworkIP(False)

	# a more condition
	def _immidiate(self):
		# condition 2 - length subnet 1 + lenght subnet 2 == bc ip of subnet 2
		return self.first.n_thIP(self.total-1, summary_calc=True) == self.second.broadcast_address()



# ----------------------------------------------------------------------------
# Main Function
# ----------------------------------------------------------------------------
if __name__ == '__main__':
	pass
# END
# ----------------------------------------------------------------------------
